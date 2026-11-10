from playwright.sync_api import Page, expect

# Helper function to avoid code duplication
def add_todo(page: Page, text: str):
    page.get_by_test_id("todo-input").fill(text)
    page.get_by_test_id("add-button").click()

def open_and_count(page: Page) -> int:
    with page.expect_response("**/api/todos") as loaded:
        page.goto("/")
    already = len(loaded.value.json())
    expect(page.get_by_test_id("todo-item")).to_have_count(already)
    return already

# 1. Test adding a new task
def test_add_todo(page: Page):
    before = open_and_count(page)
    add_todo(page, "Buy milk")
    items = page.get_by_test_id("todo-item")
    expect(items).to_have_count(before + 1)
    expect(items.last).to_contain_text("Buy milk")

def test_create_todo(api: APIRequestContext): # test for the api
    api.post("/api/reset")
    response = api.post("/api/todos", data={"text": "Learn API Testing"})
    
    # Verify the request was successful (Status 200/201)
    expect(response).to_be_ok()
    
    # Verify the server returned the created object properly
    data = response.json()
    assert data["text"] == "Learn API Testing"
    assert data["completed"] is False


# 2. Test adding an empty task (should not be added)
def test_add_empty_todo(page: Page):
    before = open_and_count(page)
    add_todo(page, "")
    expect(page.get_by_test_id("todo-item")).to_have_count(before)


# 3. Test marking a task as completed #########################################################
def test_complete_todo(page: Page):
    before = open_and_count(page)
    add_todo(page, "Do homework")
    items = page.get_by_test_id("todo-item")
    expect(items).to_have_count(before + 1)
    row = items.last
    row.get_by_test_id("todo-checkbox").click()
    expect(row.locator("span.completed")).to_be_visible()


# 4. Test deleting a task
def test_delete_todo(page: Page):
    before = open_and_count(page)
    add_todo(page, "Take out the trash")
    items = page.get_by_test_id("todo-item")
    expect(items).to_have_count(before + 1)
    items.last.get_by_test_id("delete-button").click()
    expect(items).to_have_count(before)



# 5. Test adding multiple tasks
def test_add_multiple_todos(page: Page):
    before = open_and_count(page)
    add_todo(page, "Task 1")
    add_todo(page, "Task 2")
    add_todo(page, "Task 3")
    items = page.get_by_test_id("todo-item")
    expect(items).to_have_count(before + 3)
    #expect(items.nth(0)).to_contain_text("Task 1")
    #expect(items.nth(1)).to_contain_text("Task 2")
    #expect(items.nth(2)).to_contain_text("Task 3")
