from flask import Flask, render_template, request, jsonify, redirect, url_for
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
    completed = db.Column(db.Boolean, nullable=False, default= False)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id'), nullable=False)

class TodoList(db.Model):
    __tablename__= 'todo_lists'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String, nullable= False)
    todos = db.relationship('todos', backref='todolist', lazy=True)

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

@app.route("/todo/<todo_id>/set-completed", methods=['POST'])
def set_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })


if __name__ == '__main__':
    app.run()