from flask import Flask, render_template, request, jsonify, session, send_file, abort
import requests
import os, subprocess
import uuid
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Ollama service URL (will be the service name in docker-compose)
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:11434')

# Base directory for storing summaries
SUMMARIES_BASE_DIR = Path('/tmp/summaries')

def get_or_create_session_id():
    """Get existing session ID or create a new UUIDv4"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_session_directory(session_id):
    """Get or create the directory for a session"""
    session_dir = SUMMARIES_BASE_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Get or create session ID
        session_id = get_or_create_session_id()
        get_session_directory(session_id)

        # Check if the session directory exists (could have been cleaned by cron)
        session_dir_path = SUMMARIES_BASE_DIR / session_id
        if 'session_id' in session and not session_dir_path.exists():
            # Session folder was cleaned, return specific error
            return jsonify({
                'error': 'Session expired',
                'code': 'SESSION_EXPIRED',
                'message': 'Your session folder has been cleaned. Please refresh the page to start a new session.'
            }), 410  # 410 Gone - resource no longer available

        data = request.get_json()
        user_input = data.get('text', '')

        if not user_input:
            return jsonify({'error': 'No text provided'}), 400

        # Prepare the prompt for summarization
        prompt = f"""Summarize the following text into 3-5 concise bullet points. Only provide the bullet points, nothing else:

{user_input}"""

        # Call Ollama API
        response = requests.post(
            f'{OLLAMA_URL}/api/generate',
            json={
                'model': 'llama3.2:1b',
                'prompt': prompt,
                'stream': False
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            summary = result.get('response', '')

            # Store summary in session-based directory
            session_dir = get_session_directory(session_id)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            summary_file = session_dir / f'summary_{timestamp}.txt'

            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"Original Text:\n{user_input}\n\n")
                f.write(f"Summary:\n{summary}\n")
                f.close()

            # Generate URL for the summary file
            filename = summary_file.name
            file_url = f'/summaries/{session_id}/{filename}'

            # Generate a raw summary file (with URL included)
            summary_file_raw = session_dir / f'summary_{timestamp}.raw'
            orig_text_raw_cmd = f"echo \"Original Text:\n{user_input}\n\n\" >> {summary_file_raw}"
            orig_summary_raw_cmd = f"echo \"Summary:\n{summary}\n\" >> {summary_file_raw}" 
        
            os.system(orig_text_raw_cmd)
            os.system(orig_summary_raw_cmd)
            # with open(summary_file_raw, 'w', encoding='utf-8') as f:
            #     f.write(orig_text_res)
            #     f.write(orig_summary_res)
            #     f.close()

            return jsonify({
                'summary': summary,
                'session_id': session_id,
                'file': str(summary_file),
                'url': file_url
            })
        else:
            return jsonify({'error': 'Failed to generate summary'}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'LLM service unavailable: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summaries/<session_id>/<filename>')
def get_summary_file(session_id, filename):
    """Serve summary files for a given session"""
    try:
        # Validate session_id format (UUIDv4)
        try:
            uuid.UUID(session_id, version=4)
        except ValueError:
            abort(404)

        # Validate filename format (must start with 'summary_')
        if not filename.startswith('summary_'):
            abort(404)

        # Construct file path
        file_path = SUMMARIES_BASE_DIR / session_id / filename

        # Check if file exists and is within the summaries directory
        if not file_path.exists() or not file_path.is_file():
            abort(404)

        # Verify the resolved path is still within the summaries directory (prevent path traversal)
        try:
            file_path.resolve().relative_to(SUMMARIES_BASE_DIR.resolve())
        except ValueError:
            abort(404)

        return send_file(file_path, mimetype='text/plain')

    except Exception as e:
        abort(404)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
