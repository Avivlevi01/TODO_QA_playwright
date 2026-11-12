import pytest
from playwright.sync_api import APIRequestContext, Page, expect

from tests.UI.todo_page import TodoPage


@pytest.fixture
def todos(api: APIRequestContext, page: Page, base_url: str) -> TodoPage:
    api.post("/api/reset")
    screen = TodoPage(page)
    screen.open(base_url)
    expect(screen.items).to_have_count(0)
    return screen


@pytest.mark.ui
def test_add_todo(todos: TodoPage):
    todos.add("Buy milk")
    todos.expect_texts(["Buy milk"])


@pytest.mark.ui
@pytest.mark.parametrize("text", ["", "   "])
def test_blank_text_is_not_added(todos: TodoPage, text: str):
    todos.add(text)
    expect(todos.items).to_have_count(0)


@pytest.mark.ui
def test_complete_todo(todos: TodoPage):
    todos.add("Do homework")
    todos.items.first.get_by_test_id("todo-checkbox").click()
    expect(todos.items.first.locator("span.completed")).to_be_visible()


@pytest.mark.ui
def test_delete_todo(todos: TodoPage):
    todos.add("Take out the trash")
    todos.items.first.get_by_test_id("delete-button").click()
    expect(todos.items).to_have_count(0)


@pytest.mark.ui
def test_add_multiple_todos(todos: TodoPage):
    todos.add("Task 1")
    todos.add("Task 2")
    todos.add("Task 3")
    todos.expect_texts(["Task 1", "Task 2", "Task 3"])


@pytest.mark.ui
def test_long_text_is_saved_exactly(todos: TodoPage):
    text = "x" * 200
    todos.add(text)
    todos.expect_texts([text])


@pytest.mark.ui
def test_duplicate_text_stays_as_two_rows(todos: TodoPage):
    todos.add("Buy milk")
    todos.add("Buy milk")
    todos.expect_texts(["Buy milk", "Buy milk"])


@pytest.mark.ui
def test_row_appears_after_slow_refresh(todos: TodoPage, page: Page):
    def delay_refresh(route):
        if route.request.method == "GET":
            page.wait_for_timeout(600)
        route.continue_()

    page.route("**/api/todos", delay_refresh)
    with page.expect_response(lambda r: r.request.method == "GET" and r.url.endswith("/api/todos")):
        todos.add("Buy milk")
    todos.expect_texts(["Buy milk"])


@pytest.mark.ui
def test_list_shows_error_when_get_fails(todos: TodoPage, page: Page):
    page.route("**/api/todos", lambda route: route.fulfill(status=500, body="down"))
    page.reload()
    expect(todos.load_error).to_be_visible()
    expect(todos.items).to_have_count(0)
