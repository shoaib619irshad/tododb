from flask_pymongo import PyMongo , ObjectId
from flask import Flask , request , jsonify , abort
from pymongo.errors import PyMongoError

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
    return jsonify({"data":todos ,"count":len(todos)})

#GET Route to display one todo
@app.route('/todo/<ObjectId:id>', methods=["GET"])
def display_single_todo(id):
    try:
        todo = db.todo.find_one({"_id": id})
        todo['_id']=str(todo['_id'])
        return jsonify(todo)
    except PyMongoError:
        return jsonify(error="Todo not found") , 404

#PATCH Route to update a todo
@app.route('/todo/<ObjectId:id>' , methods=["PATCH"])
def update_todo(id):
     if not request.json:
        abort(500)

     title = request.json.get("title", None)
     desc = request.json.get("description","")

     if title is None and desc == "":
        return jsonify(message="Invalid Request"), 500
     
     if desc == "" and not title is None:
         todo = db.todo.find_one_and_update({'_id': id}, {"$set": {'title': title}})
     elif title is None and desc != "":
         todo = db.todo.find_one_and_update({'_id': id}, {"$set": {'description': desc}})
     else:
         todo = db.todo.find_one_and_update({'_id': id}, {"$set": {'title': title , 'description': desc}})

     return jsonify(message="Updated Successfully")


#DELETE Route to delete a todo
@app.route('/todo/<ObjectId:id>' , methods=["DELETE"])
def delete_todo(id):
     todo = db.todo.find_one_and_delete({'_id': id})
     return jsonify(message="Deleted Successfully")