# app.py
import os
import sqlite3
from flask import Flask, request, session, redirect, url_for, render_template, g, jsonify
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

# template and static folders to the help build outout under /app/dist
app = Flask(
    __name__,
    template_folder="/app/dist/template", #template folder under dist
    static_folder="/app/dist/static" #static folder under dist
)

#session cookie stuff 
app.secret_key = os.getenv("FLASK_SECRET", os.urandom(24))
#set db path
DATABASE = os.getenv("DB_PATH", "/app/data/insecure_web.db")
conn = sqlite3.connect(DATABASE) #connect to db

#provide db connection for each req
def get_db():
    db = getattr(g, "_database", None)
    
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        
    return db

#close db conn once app tears dowbn
@app.teardown_appcontext
def close_connection(exception):
    
    db = getattr(g, "_database", None)
    if db is not None:
        
        db.close()

#homepage/default
@app.route("/")
def index():
    return render_template("login.html", logged_in=('user' in session), user=session.get("user"))

#to register page
@app.route("/register", methods=["GET", "POST"])
#submit the reg form
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        name = request.form.get("name", "").strip()
        db = get_db()

        # student id generator
        cur = db.execute("SELECT MAX(student_id) FROM users")
        row = cur.fetchone()
        new_student_id = (row[0] or 100) + 1  

        try:
            #hashes pw 
            pw_hash = generate_password_hash(password)
            #add new user to db
            #user table
            db.execute(
                "INSERT INTO users (username, password_hash, student_id) VALUES (?,?,?)",
                (username, pw_hash, new_student_id)
            )
            #profile table
            db.execute(
                "INSERT INTO profiles (student_id, name, notes) VALUES (?,?,?)",
                (new_student_id, name or username, "User-supplied notes.")
            )
            db.commit()
            
        except Exception as e:
            return f"Registration failed: {e}", 400

        return redirect(url_for("index"))

    return render_template("register.html")

#for login
@app.route("/login", methods=["POST"])

def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    db = get_db()
    cur = db.execute("SELECT username, password_hash, student_id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    
    if row and check_password_hash(row["password_hash"], password):
        session['user'] = row["username"]
        session['student_id'] = row["student_id"]
        return redirect(url_for("profile", student_id=row["student_id"]))
    
    return "Login failed", 401

#not rlly used
# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("index"))


@app.route("/profile/<int:student_id>")
def profile(student_id):
    db = get_db()
    cur = db.execute("SELECT student_id, name, notes FROM profiles WHERE student_id = ?", (student_id,))
    p = cur.fetchone()
    if not p:
        return "Profile not found", 404
    return render_template("profile.html", profile=p, user=session.get("user"))


if __name__ == "__main__":
    # Run on port 8000 
    app.run(host="0.0.0.0", port=8000, debug=False)