from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# In-memory storage. The list resets when the server stops.
todos = []
next_id = 1

# Pydantic model that validates the POST body
class TodoCreate(BaseModel):
    text: str

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
    <p id="load-error" data-testid="load-error" hidden>Could not load tasks.</p>
    <ul id="todo-list"></ul>

    <script>
        async function fetchTodos() {
            const res = await fetch('/api/todos');
            const list = document.getElementById('todo-list');
            const error = document.getElementById('load-error');
            if (!res.ok) {
                list.innerHTML = '';
                error.hidden = false;
                return;
            }
            error.hidden = true;
            const todos = await res.json();
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
                span.setAttribute('data-testid', 'todo-text');
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
            if (!input.value.trim()) return;
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

        fetchTodos();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_TEMPLATE

@app.get("/api/todos")
def get_todos():
    return todos

@app.post("/api/todos", status_code=201)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = {"id": next_id, "text": todo.text, "completed": False}
    todos.append(new_todo)
    next_id += 1
    return new_todo

@app.patch("/api/todos/{todo_id}")
def update_todo(todo_id: int):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            return todo
    raise HTTPException(status_code=404, detail="Not found")

@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    global todos
    # Rebuild the list without the deleted item
    todos = [t for t in todos if t['id'] != todo_id]
    return None

@app.post("/api/reset", status_code=201)
def reset_todos():
    global todos, next_id
    todos = []
    next_id = 1
    return {"message": "Todos reset successfully"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)