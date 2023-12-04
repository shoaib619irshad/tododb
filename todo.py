from flask_pymongo import PyMongo
from flask import Flask , request , jsonify , abort

app = Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/todo_db")
db = mongodb_client.db


@app.route('/todo',methods=["POST"])
def add_todo():
    if not request.json:
        abort(500)

    id = request.json.get("id", None)
    title = request.json.get("title",None)
    des = request.json.get("description","")
   
    if id is None or title is None:
        return jsonify(message="Invalid Request"), 500
    
    db.todo.insert_one({'id':id,'title': title, 'description': des,'done':False})
    return jsonify(message="Added Successfully")

@app.route('/todo', methods=["GET"])
def display_todo():
    todos =list(db.todo.find()) 
    for x in todos:
        x['_id']= str(x['_id'])
    return jsonify({"data":todos ,"len":len(todos)})

    
