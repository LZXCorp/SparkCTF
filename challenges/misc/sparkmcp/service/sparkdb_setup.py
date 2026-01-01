import os
import sqlite3
import secrets

db_path = os.path.join(os.path.dirname(__file__), 'spark.db')
if os.path.exists(db_path):
    os.remove(db_path)

open(db_path, 'w').close()

# Compact scope representation using a bitmask
SCOPE = {
    "read:data": 1 << 0,   # 1
    "write:data": 1 << 1,  # 2
    "admin:users": 1 << 2, # 4
}

def scopes_to_mask(scopes):
    mask = 0
    for s in scopes:
        mask |= SCOPE.get(s, 0)
    return mask

# Connect (SQLite creates the DB file if it doesn't exist)
db_conn = sqlite3.connect(db_path)
cursor = db_conn.cursor()

# Create base tables (idempotent)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        command TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS auth (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id TEXT NOT NULL,
        token TEXT NOT NULL,
        scope_mask INTEGER NOT NULL DEFAULT 0
    )
''')

# Add helpful unique indexes to keep seeding idempotent
cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_tools_name ON tools(name)")
cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_auth_client_id ON auth(client_id)")
db_conn.commit()

# Seed Tools (idempotent)
cursor.execute('''
    INSERT OR IGNORE INTO tools (name, description, command) VALUES (?, ?, ?)
''', ("Cow", "Displays SparkCTF as a cow.", "/usr/games/cowsay 'SparkCTF'"))

# Seed Auth with scope masks (UPSERT)
admin_mask = scopes_to_mask(["read:data", "write:data", "admin:users"])
guest_mask = scopes_to_mask(["read:data"])

def upsert_auth(client_id: str, token: str, mask: int):
    cursor.execute(
        '''
        INSERT INTO auth (client_id, token, scope_mask)
        VALUES (?, ?, ?)
        ON CONFLICT(client_id) DO UPDATE SET
            token=excluded.token,
            scope_mask=excluded.scope_mask
        ''',
        (client_id, token, mask)
    )

admin_token = secrets.token_urlsafe(64)
upsert_auth("admin@sparkctf.org", admin_token, admin_mask)
upsert_auth("guest", "guest", guest_mask)

# Commit and close
db_conn.commit()
db_conn.close()