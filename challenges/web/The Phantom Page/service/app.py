from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def index():
    """
    Renders the main spectral anomaly interface, using the updated template name: phantom_web.html.
    This template now contains all necessary HTML, CSS (inline), and decoy JavaScript.
    """
    # Renders the HTML template located at service/templates/phantom_web.html
    return render_template('phantom_web.html')

@app.route("/assets/ghost.js")
def ghost_script():
    """
    Serves the hidden ghost.js file from the assets directory.
    This explicit route is necessary to fulfill the preloading link and the logic of the challenge,
    making the asset discoverable via the Network tab by browser agents.
    """
    # Constructs the path to the assets folder relative to the app root
    assets_dir = os.path.join(app.root_path, 'assets')
    return send_from_directory(assets_dir, 'ghost.js')

if __name__ == "__main__":
    # Listen on 0.0.0.0:5001 to ensure it works correctly inside Docker
    app.run(host="0.0.0.0", port=5001)
