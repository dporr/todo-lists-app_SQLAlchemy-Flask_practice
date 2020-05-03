from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", data=[
        {"description": "Item 1"},
        {"description": "Second item"},
        {"description": "A third one..."},
        {"description": "4th Item"}
        ]
    )