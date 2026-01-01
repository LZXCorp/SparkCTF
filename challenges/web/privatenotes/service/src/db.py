import secrets
import bleach

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

import random
from wonderwords import RandomSentence

FLAG = "SPARK{n0_sQLi_EXp3ri3n2E?}"

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    if db is None:
        app = current_app._get_current_object()
        db = g._database = PyMongo(app).db
    return db

db = LocalProxy(lambda: get_db())

def create_user(username, password):
    user = {"username": bleach.clean(username), "password": bleach.clean(password)}
    try:
        db.users.insert_one(user)
        return True
    except DuplicateKeyError:
        return False

def verify_user(username, password):
    user = db.users.find_one({ "username": bleach.clean(username), "password": bleach.clean(password) })
    return user is not None

def create_private_notes(title, content):
    seq_doc = db.counters.find_one_and_update(
        {"_id": "notes_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    note_id = int(seq_doc["seq"])

    passphrase = secrets.token_urlsafe(16)
    note = {
        "_id": note_id,
        "title": bleach.clean(title),
        "content": bleach.clean(content),
        "passphrase": passphrase
    }
    db.notes.insert_one(note)
    return {"id": str(note_id), "passphrase": passphrase}

def get_private_note(note_id, passphrase):
    try:
        try:
            query_id = int(note_id)
        except (ValueError, TypeError):
            query_id = ObjectId(note_id)

        # prevent NoSQL Injection via passphrase
        if isinstance(passphrase, dict):
            if "$ne" in passphrase:
                return None

        note = db.notes.find_one({ "_id": query_id, "passphrase": passphrase }, { "title": 1, "content": 1, "_id": 0 })
        return note
    except (InvalidId, TypeError):
        return None

def random_note_gen(n):
    rs = RandomSentence()

    for _ in range(n):
        title = rs.sentence()  

        num_sentences = random.randint(1, 3)
        content_sentences = [rs.sentence() for _ in range(num_sentences)]
        content = " ".join(content_sentences)

        create_private_notes(title, content)

def init_db():
    try:
        db.notes.drop()
        db.notes.create_index("passphrase", unique=True)
        db.users.create_index("username", unique=True)

        random_note_gen(random.randint(2, 5))
        create_private_notes("CONFIDENTIAL NOTE", f"Here is the secret flag, do not share it with anyone!\n{FLAG}")
        random_note_gen(random.randint(2, 5))
    except OperationFailure:
        pass