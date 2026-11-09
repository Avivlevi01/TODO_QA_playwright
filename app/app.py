from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# שמירת הנתונים בזיכרון (יתאפס בכל פעם שהשרת יכבה)
todos = []
next_id = 1

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QA Todo App</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; }
        li { margin-bottom: 10px; display: flex; align-items: center; gap: 10px; }
        .completed { text-decoration: line-through; color: gray; }
    </style>
</head>
<body>
    <h1>Todo List</h1>
    <div>
        <input type="text" id="new-todo" data-testid="todo-input" placeholder="Add a new task...">
        <button onclick="addTodo()" data-testid="add-button">Add</button>
    </div>
    <ul id="todo-list"></ul>

    <script>
        async function fetchTodos() {
            const res = await fetch('/api/todos');
            const todos = await res.json();
            const list = document.getElementById('todo-list');
            list.innerHTML = '';
            
            todos.forEach(todo => {
                const li = document.createElement('li');
                li.setAttribute('data-testid', 'todo-item');

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.checked = todo.completed;
                checkbox.setAttribute('data-testid', 'todo-checkbox');
                checkbox.onclick = () => toggleTodo(todo.id);

                const span = document.createElement('span');
                span.innerText = todo.text;
                if (todo.completed) span.className = 'completed';

                const delBtn = document.createElement('button');
                delBtn.innerText = 'Delete';
                delBtn.setAttribute('data-testid', 'delete-button');
                delBtn.onclick = () => deleteTodo(todo.id);

                li.appendChild(checkbox);
                li.appendChild(span);
                li.appendChild(delBtn);
                list.appendChild(li);
            });
        }

        async function addTodo() {
            const input = document.getElementById('new-todo');
            if (!input.value) return;
            await fetch('/api/todos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: input.value})
            });
            input.value = '';
            fetchTodos();
        }

        async function toggleTodo(id) {
            await fetch(`/api/todos/${id}`, {method: 'PATCH'});
            fetchTodos();
        }

        async function deleteTodo(id) {
            await fetch(`/api/todos/${id}`, {method: 'DELETE'});
            fetchTodos();
        }

        // טעינה ראשונית של המשימות
        fetchTodos();
    </script>
</body>
</html>
"""

# מחזיר את הממשק (HTML)
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# API Endpoints
@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    global next_id
    data = request.json
    todo = {"id": next_id, "text": data.get("text", ""), "completed": False}
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            return jsonify(todo)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return '', 204

if __name__ == '__main__':
    # מפעיל את השרת על פורט 5000
    app.run(port=5000, debug=True)