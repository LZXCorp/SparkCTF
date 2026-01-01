from flask import Flask, render_template, request, jsonify
import re
import secrets

from db import create_private_notes, get_private_note, init_db

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MONGO_URI'] = 'mongodb://localhost:27017/privatenotes'

app.secret_key = secrets.token_urlsafe(128)

with app.app_context():
    init_db()

# note pages
@app.route('/', methods=['GET'])
def create_note_page():
    return render_template('create_notes.html')

@app.route('/view', methods=['GET'])
def view_note_page():
    return render_template('view_notes.html')

# notes API endpoint
@app.route('/api/create', methods=['POST'])
def create_note():
    title = request.form['title']
    content = request.form['content']
    
    if not re.match(r'^.{1,100}$', title):
        return "Title must be 1-100 characters long.", 400
    elif not re.match(r'^.{1,1000}$', content, re.DOTALL):
        return "Content must be 1-1000 characters long.", 400
    else:
        note_info = create_private_notes(title, content)
        return f'''
            <div class="note-display">
                <h3>Note Created Successfully</h3>
                <p><strong>Note ID:</strong> {note_info['id']}</p>
                <p><strong>Passphrase:</strong> {note_info['passphrase']}</p>
                <p style="color: #dc2626; margin-top: 12px;"><strong>Important:</strong> Save these credentials. You will need both to view your note.</p>
            </div>
        '''

@app.route('/api/view', methods=['POST'])
def view_note():
    data = request.get_json()
    note_id = data.get('id')
    passphrase = data.get('passphrase')
    
    if not note_id or not passphrase:
        return jsonify({"error": "Missing id or passphrase"}), 400
    
    note = get_private_note(note_id, passphrase)
    
    if note:
        return jsonify(note), 200
    else:
        return jsonify({"error": "Note not found or invalid passphrase"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
