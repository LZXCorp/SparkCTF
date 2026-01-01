-- ./data/schema.sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    student_id INTEGER UNIQUE NOT NULL
);

CREATE TABLE profiles (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    notes TEXT
);
