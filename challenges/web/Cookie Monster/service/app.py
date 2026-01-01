from flask import Flask, request, make_response, render_template, redirect, url_for
import base64
import json
import os

app = Flask(__name__)

FLAG_FILE = "/app/flag.txt"

def encode_cookie(payload: dict) -> str:
    # JSON -> bytes -> URL-safe base64 (no padding)
    j = json.dumps(payload, separators=(',',':')).encode()
    return base64.urlsafe_b64encode(j).rstrip(b"=").decode()

def decode_cookie(token: str) -> dict:
    try:
        # Add padding if necessary
        padding = '=' * (-len(token) % 4)
        b = base64.urlsafe_b64decode(token + padding)
        return json.loads(b.decode())
    except Exception:
        return {}

@app.route('/')
def index():
    # default cookie payload
    payload = {'role': 'guest'}
    token = encode_cookie(payload)

    # if the user already sent an auth cookie, prefer it (so they can return with changed cookie)
    incoming = request.cookies.get('auth')
    if incoming:
        try:
            payload = decode_cookie(incoming)
            token = incoming  # keep their token (even if modified)
        except:
            payload = {'role': 'guest'}
            token = encode_cookie(payload)

    resp = make_response(render_template('index.html', role=payload.get('role','guest')))
    resp.set_cookie('auth', token, httponly=False)  # httponly false so players can edit with JS if needed
    return resp

@app.route('/admin')
def admin():
    token = request.cookies.get('auth') or ''
    payload = decode_cookie(token)
    if payload.get('role') == 'admin':
        # reveal flag
        flag = "FLAG{missing_flag_file}"
        try:
            with open(FLAG_FILE, 'r') as f:
                flag = f.read().strip()
        except Exception:
            pass
        return render_template('admin.html', flag=flag)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
