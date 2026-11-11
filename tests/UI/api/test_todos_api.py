from playwright.sync_api import APIRequestContext, expect, Page
import pytest
from conftest import BASE_URL

# 1. Create (POST) - Test adding a new todo
@pytest.mark.api
def test_create_todo(api: APIRequestContext):
    api.post("/api/reset")
    response = api.post("/api/todos", data={"text": "Learn API Testing"})
    
    # Verify the request was successful (Status 200/201)
    expect(response).to_be_ok()
    
    # Verify the server returned the created object properly
    data = response.json()
    assert data["text"] == "Learn API Testing"
    assert data["completed"] is False

# 2. Read (GET) - Test fetching all todos
@pytest.mark.api
def test_get_todos(api: APIRequestContext):
    # Create one todo first to ensure the list isn't completely empty
    api.post("/api/reset")
    api.post("/api/todos", data={"text": "GET test"})
    
    response = api.get("/api/todos")
    expect(response).to_be_ok()
    
    # Verify we get a list back
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) > 0

# 3. Update (PATCH) - Test marking a todo as completed
@pytest.mark.api
def test_update_todo(api: APIRequestContext):
    # Create a todo to update
    api.post("/api/reset")
    create_res = api.post("/api/todos", data={"text": "To be updated"})
    todo_id = create_res.json()["id"]
    
    # Send PATCH request to update it
    patch_res = api.patch(f"/api/todos/{todo_id}")
    expect(patch_res).to_be_ok()
    
    # Verify the 'completed' status flipped to True
    assert patch_res.json()["completed"] is True

# 4. Delete (DELETE) - Test removing a todo
@pytest.mark.api
def test_delete_todo(api: APIRequestContext):
    # Create a todo to delete
    api.post("/api/reset")
    create_res = api.post("/api/todos", data={"text": "To be deleted"})
    todo_id = create_res.json()["id"]
    
    # Send DELETE request
    delete_res = api.delete(f"/api/todos/{todo_id}")
    
    # DELETE requests often return status 204 (No Content)
    assert delete_res.status == 204
    
    # Verify it's actually gone by trying to update it
    patch_res = api.patch(f"/api/todos/{todo_id}")
    assert patch_res.status == 404

# 5. Negative Test - Try to update a non-existent ID
@pytest.mark.api
def test_update_non_existent_todo(api: APIRequestContext):
    # ID 99999 does not exist
    api.post("/api/reset")
    response = api.patch("/api/todos/99999")
    
    # Verify the server correctly rejects it with a 404 status
    assert response.status == 404


def reset_and_open(api: APIRequestContext, page: Page): # helper function for the tests
    # This helper is not a test. Pytest never calls it on its own.
    # It runs only when a test function calls it.
    api.post("/api/reset")
    # The page fixture has no base address unless you pass --base-url.
    # The tab starts at about:blank, so goto("/") is an invalid URL.
    # BASE_URL is the full address the api fixture already uses.
    page.goto(f"{BASE_URL}/")

@pytest.mark.api
def test_page_is_empty_after_reset(api: APIRequestContext, page: Page): # test for the ui and api
    # Pytest calls this because the name starts with test_.
    # The parameter names api and page make Pytest call those fixtures
    # first, then pass the results into this function.
    reset_and_open(api, page)
    expect(page.get_by_test_id("todo-item")).to_have_count(0)


@pytest.mark.api
def test_add_in_ui_then_delete_in_api(api: APIRequestContext, page: Page): # test for the ui and api
    # Pytest calls this because the name starts with test_.
    # The names api and page make Pytest build both tools first.
    reset_and_open(api, page)

    page.get_by_test_id("todo-input").fill("Buy milk")
    page.get_by_test_id("add-button").click()
    expect(page.get_by_test_id("todo-item")).to_contain_text("Buy milk")

    # The button click saved the task on the server.
    # The API read proves that, and gives the id for the delete.
    todos = api.get("/api/todos").json()
    assert len(todos) == 1
    assert todos[0]["text"] == "Buy milk"

    delete_res = api.delete(f"/api/todos/{todos[0]['id']}")
    assert delete_res.status == 204
    assert api.get("/api/todos").json() == []

    # The open tab keeps the old row until it loads the page again.
    page.reload()
    expect(page.get_by_test_id("todo-item")).to_have_count(0)

