from flask import Flask, render_template_string, render_template, request 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/solution", methods=["POST"])
def solution():
    guess = request.form.get("solution")
    rendered = f"<h1>I dont know math, I cant tell if {guess} is correct! (maybe try again with the correct answer to 3 d.p. ?)</h1>"
    return render_template_string(rendered)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=2509)