# QA Automation Portfolio Project: Todo App

[![Automated Tests](https://github.com/Avivlevi01/TODO_QA_playwright/actions/workflows/tests.yml/badge.svg)](https://github.com/Avivlevi01/TODO_QA_playwright/actions)

End-to-end UI and API test suite for a small todo app, built with Playwright (Python) and pytest.

## 🎯 What is Tested
* **UI (End-to-End):** User journeys including adding new tasks, attempting to add empty tasks (negative test), marking tasks as complete, and deleting tasks.
* **API (Backend Logic):** Full CRUD operations (GET, POST, PATCH, DELETE) and negative scenarios (e.g., verifying 404 status codes for non-existent items).

## 🛠️ Tech Stack
* **Python 3.9+**
* **Pytest** (Test runner & assertions)
* **Playwright** (Browser automation & API context)
* **FastAPI & Uvicorn** (Local application server under test)
* **Git** (Version control)

## 📁 Project Structure
```text
TODO_QA_playwright/
├── app/
│   └── app.py                 # Local FastAPI server & HTML UI
├── tests/
│   ├── api/
│   │   └── test_todos_api.py  # API test scenarios
│   └── ui/
│       └── test_todos_ui.py   # UI test scenarios
├── conftest.py                # Pytest fixtures (e.g., APIRequestContext)
├── pytest.ini                 # Pytest configuration, base URL, and markers
├── requirements.txt           # Project dependencies
└── README.md
```

## 🚀 How to Run

**1. Setup Environment**
Clone the repository, create a virtual environment, and install dependencies:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

**2. Start the Local Server**
The app needs to run in the background for the tests to work. Open a terminal and run:
```bash
python app/app.py
```
*(The app is now available at http://localhost:5000 and the Swagger API docs at http://localhost:5000/docs)*

**3. Run the Tests**
Open a **new** terminal (keep the server running) and run:

* **Run everything (API + UI):** 
  ```bash
  pytest
  ```
* **Run API tests only:** 
  ```bash
  pytest -m api
  ```
* **Run UI tests visually (slowed down for observation):** 
  ```bash
  pytest -m ui --headed --slowmo 500
  ```
* **Run UI tests with debug tracing (saves trace.zip and screenshot on failure):** 
  ```bash
  pytest -m ui --tracing retain-on-failure --screenshot only-on-failure
  ```

## 💡 Design Notes
* **`data-testid` attributes:** UI locators strictly use `data-testid` instead of CSS classes or XPaths. This decouples the tests from the design/styling, making them highly resilient to UI changes.
* **API vs. UI Testing:** API tests bypass the browser to directly test business logic, providing extremely fast and stable feedback. UI tests are reserved for verifying actual user workflows and DOM interactions.
* **Test Isolation:** Pytest fixtures ensure a clean, isolated context (like incognito mode) for every test run to prevent data leakage and side effects between tests.

## 🚀 Possible Next Steps
* Integrate a **CI/CD pipeline** (e.g., GitHub Actions) to run tests automatically on every push.
* Expand coverage with **Cross-Browser Testing** (Firefox, WebKit).
* Migrate or duplicate the automation framework into **TypeScript**.