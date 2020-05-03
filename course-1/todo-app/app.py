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
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgress://{user}:{password}@{host}:5432/{schema}'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String, nullable= False)

db.create_all()

@app.route('/')
def index():
    return render_template("index.html", data=Todo.query.all())

if __name__ == '__main__':
    app.run()