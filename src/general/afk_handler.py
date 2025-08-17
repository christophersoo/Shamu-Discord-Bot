from datetime import datetime, timezone
import discord

class AFK_Handler():
    def __init__(self, interaction, reason, conn, cursor):
        self.interaction = interaction
        self.reason = reason
        self.conn = conn
        self.cursor = cursor
        print("AFK handler initialised.")

    async def run(self):
        print("bot running")
        name = self.interaction.user.nick
        if name is None:
            name = self.interaction.user.name
        print(f"{name} name fetched.")

        self.cursor.execute("""DELETE FROM afk_logs WHERE user_id = %s""", (self.interaction.user.id, ))
        self.conn.commit()

        self.cursor.execute("""SELECT * FROM afk_users WHERE user_id = %s""", (self.interaction.user.id, ))
        if self.cursor.fetchone():
            await self.interaction.response.send_message("You are already AFK.")
        else:
            message = f"You are now AFK.\nDo `/reason` for reason."
            since = datetime.now(timezone.utc).isoformat()

            try:
                self.cursor.execute("""
                    INSERT INTO afk_users (user_id, reason, since, nickname)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        reason = VALUES(reason),
                        since = VALUES(since),
                        nickname = VALUES(nickname)
                """, (self.interaction.user.id, self.reason, since, name))
                self.conn.commit()
            except Exception as e:
                print("Database error:", e)

            await self.interaction.user.edit(nick=f"[AFK] {name}")
            await self.interaction.response.send_message(message)
    

class AFK_Listener():
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def is_afk(self, user_id: int):
        self.cursor.execute("SELECT reason FROM afk_users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    async def remove_afk(self, member: discord.Member):
        self.cursor.execute("SELECT nickname FROM afk_users WHERE user_id = %s", (member.id,))
        nick_name = self.cursor.fetchone()
        str_nick = member.name
        if nick_name is None:
            print("bug ping")
        else:
            str_nick = nick_name[0]
    
        self.cursor.execute("DELETE FROM afk_users WHERE user_id = %s", (member.id,))
        self.conn.commit()
        await member.edit(nick=str_nick)
    
    def get_time(self, user_id):
        self.cursor.execute("""SELECT since FROM afk_users WHERE user_id = %s""", (user_id,))
        time = self.cursor.fetchone()
        if time is None:
            return None
        time_str = time[0]
        since_dt = datetime.fromisoformat(time_str) 
        time_diff = datetime.now(timezone.utc) - since_dt
        days, remainder = divmod(time_diff.total_seconds(), 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        return [days, hours, minutes, seconds]

    def log_mention(self, afk_user_id: int, message_obj):
        timestamp = int(message_obj.created_at.timestamp())
        self.cursor.execute("""
            INSERT INTO afk_logs (user_id, mentioner_id, timestamp, content)
            VALUES (%s, %s, %s, %s)
        """, (afk_user_id, message_obj.author.id, timestamp, message_obj.content))
        self.conn.commit()
    
    def get_logs(self, user_id: int):
        print(user_id)
        self.cursor.execute(
            """SELECT mentioner_id, content, timestamp FROM afk_logs WHERE user_id = %s""", (user_id,)
        )
        rows = self.cursor.fetchall()

        msg = ""

        if not rows:
            msg += "No one mentioned you while you were AFK."

        for row in rows:
            now_ts = int(datetime.now(timezone.utc).timestamp())
            seconds = now_ts - row[2]

            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)

            parts = []
            if hours > 0:
                parts.append(f"{hours}h")
            if minutes > 0:
                parts.append(f"{minutes}m")
            if seconds > 0 or not parts:
                parts.append(f"{seconds}s")

            relative_time = " ".join(parts) + " ago"
            msg += f"from: <@{row[0]}>\ncontent: {row[1]}\ntime: {relative_time}\n\n"
        
        print(msg)
        
        return msg


    
if __name__ == "__main__":
    pass
