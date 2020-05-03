from flask import Flask, render_template
from sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

#Here we better implement a sectrets manager, but by now this is OK.
#TODO: Implement a hashicorp vault cluster un integrate this app with it
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
schema = os.getenv("APP_SCHEMA")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgress://{user}:{password}@{host}:5432/{schema}'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html", data=[
        {"description": "Item 1"},
        {"description": "Second item"},
        {"description": "A third one..."},
        {"description": "4th Item"}
        ]
    )

if __name__ == '__main__':
    app.run()