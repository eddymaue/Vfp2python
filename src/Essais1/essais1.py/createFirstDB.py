# Créer une nouvelle table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT UNIQUE,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
