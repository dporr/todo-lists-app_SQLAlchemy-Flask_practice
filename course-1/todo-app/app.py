from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, sys

app = Flask(__name__)

#Here we better implement a sectrets manager, but by now this is OK.
#TODO: Implement a hashicorp vault cluster un integrate this app with it
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
schema = os.getenv("APP_SCHEMA")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:5432/{schema}'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String, nullable= False)

@app.route('/')
def index():
    return render_template("index.html", data=Todo.query.all())

@app.route("/todo/create", methods=["POST"])
def create():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description= description)
        db.session.add(todo)
        db.session.commit()
        body["description"] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error: return jsonify(body)

if __name__ == '__main__':
    app.run()