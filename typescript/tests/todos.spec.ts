import { test, expect } from "@playwright/test";
import { TodoPage } from "../pages/todo.page";

test.beforeEach(async ({ request, page }) => {
  await request.post("/api/reset");
  await page.goto("/");
});

test("adds one task", async ({ page }) => {
  const todos = new TodoPage(page);
  await todos.add("Buy milk");
  await todos.expectTexts(["Buy milk"]);
});

test("does not add a blank task", async ({ page }) => {
  const todos = new TodoPage(page);
  await todos.add("   ");
  await expect(todos.items).toHaveCount(0);
});
