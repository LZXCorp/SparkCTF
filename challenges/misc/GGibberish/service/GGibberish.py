from flask import Flask, send_file
import ggwave, random, wave, io

app = Flask(__name__)

# ROT cipher function
def rot(rotation, phrase):
    abc_lower = "abcdefghijklmnopqrstuvwxyz"
    abc_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = ''
    for char in phrase:
        if char.isalpha():
            if char.islower():
                out += abc_lower[(abc_lower.find(char)+rotation)%26]
            else:
                out += abc_upper[(abc_upper.find(char)+rotation)%26]
        else:
            out += char
    return out

@app.route("/")
def download_wav():
    # Initialize ggwave
    instance = ggwave.init()

    # Random rotation
    flag = 'SPARK{gg_not_truly_gibberish}'
    num = random.randint(1, 12)
    result = rot(num, flag)

    # Encode with ggwave
    waveform = ggwave.encode(result, protocolId=1, volume=20)

    # Save to in-memory buffer
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as f:
        f.setnchannels(1)       # Mono
        f.setsampwidth(4)       # 32-bit float
        f.setframerate(48000)   # Sample rate
        f.writeframes(waveform)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="secret.wav",
        mimetype="audio/wav"
    )
# run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=24682)
