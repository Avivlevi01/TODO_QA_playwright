import { expect, Locator, Page } from "@playwright/test";

export class TodoPage {
  readonly items: Locator;

  constructor(private readonly page: Page) {
    this.items = page.getByTestId("todo-item");
  }

  async add(text: string) {
    await this.page.getByTestId("todo-input").fill(text);
    await this.page.getByTestId("add-button").click();
  }

  async expectTexts(texts: string[]) {
    await expect(this.page.getByTestId("todo-text")).toHaveText(texts);
  }
}
