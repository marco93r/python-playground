from flask import Flask, request

app = Flask(__name__)

todos = []

@app.route('/todos', methods = ['GET'])
def get_todos():
    return todos, 200

@app.route('/todos', methods = ['POST'])
def post_todos():
    payload = request.json
    
    if "title" in payload:
        
        todo = {
            "id": len(todos) + 1,
            "title": payload["title"],
            "done": False
        }
        todos.append(todo)
        return todo, 201
    else:
        return {"error": "title required"}, 400
    
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    for t in todos:
        if t['id'] == id:
            todos.remove(t)
            return {"message": "deleted"}, 200
    return {"error": "id not found"}, 404

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    for t in todos:
        if t['id'] == id:
            t['done'] = True
            return {"message": "updated"}, 200
    return {"error": "id not found"}, 404
    


if __name__ == '__main__':
    app.run(debug=True)
