from flask_pymongo import PyMongo , ObjectId
from flask import Flask , request , jsonify , abort

app = Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/todo_db")
db = mongodb_client.db

#POST Route to add a todo
@app.route('/todo',methods=["POST"])
def add_todo():
    if not request.json:
        abort(500)

    title = request.json.get("title",None)
    des = request.json.get("description","")
   
    if title is None:
        return jsonify(message="Invalid Request"), 500
    
    db.todo.insert_one({'title': title, 'description': des,'done':False})
    return jsonify(message="Added Successfully")

#GET Route to display all todos
@app.route('/todo', methods=["GET"])
def display_todo():
    todos =list(db.todo.find()) 
    for x in todos:
        x['_id']= str(x['_id'])
    return jsonify({"data":todos ,"len":len(todos)})

#GET Route to display one todo
@app.route('/todo/<ObjectId:id>', methods=["GET"])
def display_single_todo(id):
    todo = db.todo.find_one({"_id": id})
    todo['_id']=str(todo['_id'])
    return jsonify(todo)

#PUT Route to update a todo
@app.route('/todo/<ObjectId:id>' , methods=["PUT"])
def update_todo(id):
     if not request.json:
        abort(500)

     title = request.json.get("title",None)

     if title is None:
        return jsonify(message="Invalid Request"), 500
     
     todo = db.todo.find_one_and_update({'_id': id}, {"$set": {'title': title}})
     return jsonify(message="Updated Successfully")


#DELETE Route to delete a todo
@app.route('/todo/<ObjectId:id>' , methods=["DELETE"])
def delete_todo(id):
     todo = db.todo.find_one_and_delete({'_id': id})
     return jsonify(message="Deleted Successfully")