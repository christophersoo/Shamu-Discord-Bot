def create(obj):
    obj.afkcursor.execute("""
        CREATE TABLE IF NOT EXISTS afk_users (
        user_id BIGINT PRIMARY KEY,
        reason TEXT,
        since TEXT,
        nickname TEXT
    )
    """)
    obj.afkcursor.execute("""
    CREATE TABLE IF NOT EXISTS afk_logs (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        user_id INTEGER,
        mentioner_id INTEGER,
        timestamp INTEGER,
        content TEXT
    )
    """)
    obj.afkdb.commit()
    obj.afkcursor.execute("SHOW TABLES")

    tables = obj.afkcursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0]) 