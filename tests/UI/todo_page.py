from playwright.sync_api import Page, expect


class TodoPage:
    def __init__(self, page: Page):
        self.page = page
        self.task_input = page.get_by_test_id("todo-input")
        self.add_button = page.get_by_test_id("add-button")
        self.items = page.get_by_test_id("todo-item")
        self.texts = page.get_by_test_id("todo-text")
        self.load_error = page.get_by_test_id("load-error")

    def open(self, base_url: str):
        self.page.goto(base_url)

    def add(self, text: str):
        self.task_input.fill(text)
        self.add_button.click()

    def expect_texts(self, texts: list[str]):
        expect(self.texts).to_have_text(texts)
