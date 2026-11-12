import pytest
from playwright.sync_api import Playwright, APIRequestContext

BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="session")
def base_url() -> str:
    # Replaces Playwright's class-method fixture, which pytest 9 warns about.
    return BASE_URL

@pytest.fixture(scope="session")
def api(playwright: Playwright) -> APIRequestContext:
    ctx = playwright.request.new_context(base_url=BASE_URL)
    yield ctx
    ctx.dispose()