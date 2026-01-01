import base64
import json
import os
import time
import uuid
from datetime import datetime, timedelta

import jwt
from flask import Flask, g, jsonify, render_template, request, send_from_directory

app = Flask(__name__, static_folder='css', static_url_path='/static')

valid_cookies = {}
session_states = {}

# flags
FLAG_1 = "SPARK{SP4RK_h3AdErs_0P3N}"
FLAG_2 = "SPARK{3AS1lY_D0WNgr2d1ng_P1N}"
FLAG_3 = "SPARK{PR0T0C0L_sP14RK_FUTUR3_t1m3_mAch1N3}"

# credentials
VALID_USERNAME = 'spark'
VALID_PASSWORD = 'password123'
PASSKEY_ATTEMPTS = 4
PIN_CODE = '0004'

# passkey data
FAKE_PASSKEY_UUID = 'a7f4f1c0-7ebb-46ee-b1d0-e0a977708c9b'
FAKE_PASSKEY_SESSION_ID = '5542c141-cd8c-4dd7-80e9-5a017d0adf99'
FAKE_USER_HANDLE = 'JQEUKwSJToyp8MaObd_8xw'
FAKE_CREDENTIAL_ID = 'iZLm9gu32a4IqCUPJUW3AiqLmne-1PRCkAkmiTSY9j0'
PASSKEY_ERROR_MSG = 'WebAuthn attestation rejected. Virtual security key signature mismatch.'

# jwt config
JWT_SECRET = "SP4RK"
JWT_ALGORITHM = 'HS256'

# cookie config
USER_SESSION_COOKIE = 'user_session'
USER_SESSION_TTL = 15 * 60

def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def _b64decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _generate_challenge() -> str:
    return _b64encode(os.urandom(32))


def _rp_id() -> str:
    host = request.host.split(':')[0]
    return host or 'localhost'


def _cleanup_session(cookie_value: str) -> None:
    """Remove session artifacts when cookies expire."""
    valid_cookies.pop(cookie_value, None)
    session_states.pop(cookie_value, None)


def _get_session_state(session_id: str) -> dict:
    default_state = {
        'login_complete': False,
        'passkey_attempts': 0,
        'pin_ready': False,
        'pin_verified': False,
        'token': None,
        'passkey_failed': False,
        'passkey_id': None,
        'auth_challenge': None,
        'user_handle': None,
    }
    return session_states.setdefault(session_id, default_state.copy())


def _generate_jwt(username: str) -> str:
    payload = {
        'sub': username,
        'challenge': 'PROTOCOLSP4RK',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'flag': FLAG_2,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def _decode_user_session():
    token = request.cookies.get(USER_SESSION_COOKIE)
    if not token:
        return None
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None


def _handle_passkey_failure(state: dict, retry_message: str):
    """Increment attempts and issue either retry or fallback response."""
    state['passkey_attempts'] += 1
    if state['passkey_attempts'] < PASSKEY_ATTEMPTS:
        return jsonify({
            'status': 'retry',
            'message': retry_message,
            'webauthn': True,
            'attempt': state['passkey_attempts'],
        }), 401

    state['pin_ready'] = True
    state['passkey_failed'] = True
    return jsonify({
        'status': 'alt',
        'message': 'Authenticator unavailable. Alternate vector unlocked.',
        'webauthn': True,
        'attempt': state['passkey_attempts'],
    }), 200


@app.before_request
def before_request_func():
    # Validate an existing cookie if present (15-minute TTL)
    cookie = request.cookies.get('session_id')
    if cookie and cookie in valid_cookies:
        creation_time = valid_cookies[cookie]
        if time.time() - creation_time < 15 * 60:
            g.session_id = cookie
            return
        # expired session, clean up
        _cleanup_session(cookie)

    # Check for special HTTP type (i.e. GET, POST): SP4RK
    if request.method == 'SP4RK':
        # Generate a new session cookie
        new_cookie = str(uuid.uuid4())
        valid_cookies[new_cookie] = time.time()
        session_states[new_cookie] = _get_session_state(new_cookie)
        g.new_session_cookie = new_cookie
        return jsonify({'message': 'New session created', 'session_id': new_cookie}), 200

    # Otherwise, block access
    return jsonify({'error': 'Invalid or expired session'}), 403


@app.after_request
def after_request_func(response):
    new_cookie = getattr(g, 'new_session_cookie', None)
    if new_cookie:
        response.set_cookie('session_id', new_cookie, max_age=15 * 60, httponly=True, samesite='Lax', path='/')
    return response


@app.route('/')
def index():
    decoded = _decode_user_session()
    if decoded:
        return render_template('home.html', username=decoded.get('sub', 'operator'))

    return render_template(
        'index.html',
        flag1=FLAG_1,
        passkey_uuid=FAKE_PASSKEY_UUID,
        passkey_limit=PASSKEY_ATTEMPTS,
    )


@app.route('/static/js/<path:filename>')
def static_js(filename):
    """Serve JS assets that live outside the default CSS static folder."""
    return send_from_directory(os.path.join(app.root_path, 'js'), filename)


@app.route('/login', methods=['POST'])
def login():
    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({'error': 'Session missing'}), 403

    payload = request.get_json(silent=True) or request.form
    username = (payload.get('username') or '').strip()
    password = payload.get('password') or ''

    if username.lower() != VALID_USERNAME:
        return jsonify({'error': 'Unknown user'}), 401

    if password != VALID_PASSWORD:
        return jsonify({'error': 'Invalid password'}), 401

    state = _get_session_state(session_id)
    state.update({
        'login_complete': True,
        'passkey_attempts': 0,
        'pin_ready': False,
        'pin_verified': False,
        'token': None,
        'passkey_failed': False,
        'passkey_id': FAKE_CREDENTIAL_ID,
        'auth_challenge': None,
    })
    state['user_handle'] = FAKE_USER_HANDLE

    return jsonify({'status': 'ok', 'next': 'passkey'}), 200


@app.route('/passkey/assert/options', methods=['POST'])
def passkey_assert_options():
    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({'error': 'Session missing'}), 403

    state = _get_session_state(session_id)
    if not state.get('login_complete'):
        return jsonify({'error': 'Login required first'}), 400

    credential_id = state.get('passkey_id') or FAKE_CREDENTIAL_ID
    state['passkey_id'] = credential_id

    challenge = _generate_challenge()
    state['auth_challenge'] = challenge

    options = {
        'challenge': challenge,
        'rpId': _rp_id(),
        'allowCredentials': [
            {
                'type': 'public-key',
                'id': credential_id,
                'transports': ['internal', 'hybrid'],
            }
        ],
        'timeout': 45000,
        'userVerification': 'required',
    }

    return jsonify({'options': options}), 200


@app.route('/passkey/assert', methods=['POST'])
@app.route('/passkey', methods=['POST'])
def passkey():
    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({'error': 'Session missing'}), 403

    state = _get_session_state(session_id)
    if not state.get('login_complete'):
        return jsonify({'error': 'Login required first'}), 400

    if state.get('pin_verified'):
        return jsonify({'status': 'ok', 'message': 'Already verified', 'next': 'pin-complete'}), 200

    if not state.get('auth_challenge'):
        return jsonify({'error': 'No active challenge'}), 400

    payload = request.get_json(silent=True) or {}
    assertion = payload.get('assertion') or {}
    response = assertion.get('response') or {}

    client_data_b64 = response.get('clientDataJSON')
    if not client_data_b64:
        return jsonify({'error': 'Missing client data'}), 400

    try:
        client_data = json.loads(_b64decode(client_data_b64).decode('utf-8'))
    except (ValueError, json.JSONDecodeError):
        return jsonify({'error': 'Malformed client data'}), 400

    if client_data.get('challenge') != state.get('auth_challenge'):
        return jsonify({'error': 'Challenge mismatch'}), 400

    if client_data.get('type') != 'webauthn.get':
        return jsonify({'error': 'Unexpected client data'}), 400

    if assertion.get('id') != state.get('passkey_id'):
        return jsonify({'error': 'Unknown credential'}), 400

    fingerprint = assertion.get('fingerprint') or payload.get('fingerprint')
    if fingerprint != FAKE_PASSKEY_UUID:
        return jsonify({'error': 'Fingerprint mismatch'}), 400

    state['auth_challenge'] = None

    return _handle_passkey_failure(state, PASSKEY_ERROR_MSG)


@app.route('/passkey/cancel', methods=['POST'])
def passkey_cancel():
    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({'error': 'Session missing'}), 403

    state = _get_session_state(session_id)
    if not state.get('login_complete'):
        return jsonify({'error': 'Login required first'}), 400

    if state.get('pin_ready'):
        return jsonify({
            'status': 'alt',
            'message': 'Authenticator unavailable. Alternate vector unlocked.',
            'webauthn': True,
            'attempt': state.get('passkey_attempts', PASSKEY_ATTEMPTS),
        }), 200

    payload = request.get_json(silent=True) or {}
    reason = (payload.get('reason') or '').strip() or 'Authenticator dismissed before completing attestation.'
    state['auth_challenge'] = None

    return _handle_passkey_failure(state, reason)


@app.route('/pin', methods=['POST'])
def pin_login():
    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({'error': 'Session missing'}), 403

    state = _get_session_state(session_id)
    if not state.get('pin_ready'):
        return jsonify({'error': 'Backup verification not available yet'}), 400

    payload = request.get_json(silent=True) or request.form
    pin = (payload.get('secret') or payload.get('pin') or '').strip()

    if pin != PIN_CODE:
        return jsonify({'error': 'Invalid pin'}), 401

    token = _generate_jwt(VALID_USERNAME)
    state.update({'pin_verified': True, 'token': token})

    response = jsonify({
        'status': 'ok',
        'token': token,
        'user': VALID_USERNAME,
        'flag': FLAG_2,
        'redirect': '/',
    })
    response.set_cookie(
        USER_SESSION_COOKIE,
        token,
        max_age=USER_SESSION_TTL,
        httponly=True,
        samesite='Lax',
        path='/'
    )
    return response


@app.route('/profile')
def profile():
    auth_header = request.headers.get('Authorization', '')
    token = None
    if auth_header.lower().startswith('bearer '):
        token = auth_header.split(' ', 1)[1].strip()
    token = token or request.args.get('token', '').strip()

    if not token:
        return jsonify({'error': 'Token required'}), 400

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return jsonify({'error': 'Invalid token'}), 401

    return jsonify({'status': 'ok', 'user': decoded.get('sub'), 'challenge': decoded.get('challenge')}), 200


@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'status': 'ok'})
    response.delete_cookie(USER_SESSION_COOKIE, path='/')
    return response


@app.route('/flag')
def flag():
    decoded = _decode_user_session()
    if not decoded:
        return '', 404
    username = (decoded.get('sub') or '').strip()
    if username.lower() == 'admin':
        return render_template('flag.html', flag=FLAG_3)
    return render_template('flag.html', flag=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
