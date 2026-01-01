# init_db.py
import os
import sqlite3
import random
import string
from werkzeug.security import generate_password_hash

#setting db/schema path
DB_PATH = os.getenv("DB_PATH", "/app/data/insecure_web.db")
SCHEMA_PATH = os.getenv("SCHEMA_PATH", "/app/data/schema.sql")
FLAG = os.getenv("FLAG", "SPARK{g0tt4_b3_53cure}") 

#create db frm schema
def create_db_from_schema(db_path, schema_path):
    print("[init_db] creating DB at", db_path)
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
        
    cur.executescript(sql)
    
    conn.commit()
    conn.close()
    
    # print("[init_db] schema executed")


#gen users
def generate_random_user():
    # random username (5-8 characters)
    username = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 8)))
    
    # random pass (8-12 characters n mix of letters and no.)
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))
    
    # random ID(1-11)
    student_id = random.randint(1, 11)
    
    # random name 
    first_names = ["Michael", "Jordan", "Jesse", "Casey", "Bruce", "Peter", "Miles", "Quincy", "Gustavo" , "River", "Clark"]
    last_names = ["Scofield", "Johnson", "Pinkman", "Brady", "Wayne", "Parker", "Morales", "Fring", "Rodriguez", "Martinez", "Kent"]
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # random notes
    note_templates = [
        "Loves programming and basketball",
        "Enjoys watching Dr. House",
        "Thinks LeBron is the GOAT",
        "Interested in computer science",
        "Enjoys reading, but not writing",
        "Loves sleeping",
        "Interested in red teaming",
        "Enjoys web challenges",
        "Passionate about sports, especially the lakers!",
        "Loves Andy Warhol's artworks",
        "Loves playing the piano!"
    ]
    notes = random.choice(note_templates)
    
    return username, password, student_id, name, notes

#adding the users
def seed_users(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    def add_user(username, plain_pw, sid, name, notes):
        pw_hash = generate_password_hash(plain_pw)
        cur.execute(
            "INSERT INTO users (username, password_hash, student_id) VALUES (?,?,?)",
            (username, pw_hash, sid)
        )
        cur.execute(
            "INSERT INTO profiles (student_id, name, notes) VALUES (?,?,?)",
            (sid, name, notes)
        )
    
    # generate random users
    used_student_ids = set() #create empty set -> make sure we dont reuse 
    used_usernames = set()
    
    for i in range(11):
        # keeps on  generating until we get unique username and student_id
        while True:
            username, password, student_id, name, notes = generate_random_user()
            if username not in used_usernames and student_id not in used_student_ids:
                used_usernames.add(username)
                used_student_ids.add(student_id)
                break
        
        # print(f"[init_db] Creating user: {username} (ID: {student_id}) - Password: {password}")
        add_user(username, password, student_id, name, notes)
    
    #real flag
    add_user("scruby", "qzxGuo812lebronDoncic", 12, "Scruby Sponge", f"Not so secure.. {FLAG}")
    # red herrings
    add_user("admin", "qzxGuo20lebronDoncic", 13, "Administrator", f"the flag is not here ;)")
    add_user("lecturer1", "qzxGuo19lebronDoncic", 14, "Lecturer 1", f"the flag is not here ;)")
    add_user("lecturer2", "qzxGuo196lebronDoncic", 15, "Lecturer 2", f"the flag is not here ;)")

    
    conn.commit()
    conn.close()
    

def main():
    # always recreate the database to get fresh random users -> basically refreshes every time it goes down/up
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    create_db_from_schema(DB_PATH, SCHEMA_PATH)
    seed_users(DB_PATH)

if __name__ == "__main__":
    main()
