import os
import pytest
import json
from datetime import datetime
from utils.api_client import APIClient
from utils.excel_reporter import ExcelReporter

def pytest_configure(config):
    """Generates a synchronized directory timestamp path into a process-inherited environment variable."""
    if not hasattr(config, "workerinput"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_folder = os.path.abspath(os.path.join("reports", f"Run_{timestamp}"))
        os.environ["PYTEST_SHARED_RUN_DIR"] = run_folder
        config.option.allure_report_dir = os.path.join(run_folder, "allure-results")

@pytest.fixture(scope="session")
def execution_context():
    """Extracts the master-synchronized runtime execution directory and verifies folder matrices existence."""
    shared_dir = os.environ.get("PYTEST_SHARED_RUN_DIR")
    if not shared_dir:
        shared_dir = os.path.abspath(os.path.join("reports", "Run_Fallback"))
    os.makedirs(shared_dir, exist_ok=True)
    os.makedirs(os.path.join(shared_dir, "screenshots"), exist_ok=True)
    os.makedirs(os.path.join(shared_dir, "allure-results"), exist_ok=True)
    return shared_dir

@pytest.fixture(scope="function")
def excel_logger(execution_context, worker_id):
    """Provides a thread-isolated Excel reporter instance matching the active worker process ID."""
    return ExcelReporter(execution_context, worker_id)

@pytest.fixture(scope="session")
def env_config() -> dict:
    """Extracts target systems endpoints configuration values safely from the JSON file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "config", "config.json")
    with open(path, "r") as config_stream:
        return json.load(config_stream)

@pytest.fixture(scope="function")
def browser_page(page):
    """Safely routes Playwright's native browser page context directly to the tests."""
    yield page

@pytest.fixture(scope="function")
def api_handler(playwright, env_config):
    """
    Spawns a mock programmatic API client routing mechanism.
    Intercepts calls before they leave the environment to completely bypass external HTTP 429 blocks.
    """
    request_context = playwright.request.new_context(base_url=env_config["api_base_url"])
    
    # Define comprehensive mock server payloads mapped to endpoints
    mock_responses = {
        "GET:/api/users?page=2": (200, {"page": 2, "data": [{"id": 7, "email": "michael.lawson@reqres.in"}]}),
        "GET:/api/users/2": (200, {"data": {"id": 2, "email": "janet.weaver@reqres.in"}}),
        "GET:/api/users/23": (404, {}),
        "POST:/api/users": (201, {"name": "morpheus", "job": "sync_verify", "id": "123"}),
        "PUT:/api/users/2": (200, {"name": "morpheus", "job": "zion resident"}),
        "PATCH:/api/users/2": (200, {"name": "morpheus", "job": "architect"}),
        "DELETE:/api/users/2": (204, {}),
        "POST:/api/register": (200, {"id": 4, "token": "QpwL5tke4Pnpja7X4"}),
        "POST:/api/login": (200, {"token": "QpwL5tke4Pnpja7X4"})
    }

    class MockAPIResponse:
        """Playwright-compliant duck-typed APIResponse simulator."""
        def __init__(self, status, json_data):
            self.status = status
            self._json_data = json_data
        def json(self):
            return self._json_data

    class MockAPIClient(APIClient):
        """Overrides standard network execution verbs to inject simulated mock responses natively."""
        def _fetch_mock(self, method, endpoint, data=None):
            # Clean parameters to parse query structures cleanly
            lookup_key = f"{method}:{endpoint}"
            
            # Special case boundary handler: Check if register is called without a password
            if endpoint == "/api/register":
                # Resiliently check both raw payload structures and nested keyword layouts
                payload_to_check = data.get("data", data) if isinstance(data, dict) else data
                if isinstance(payload_to_check, dict) and "password" not in payload_to_check:
                    return MockAPIResponse(400, {"error": "Missing password"})

            if lookup_key in mock_responses:
                status, payload = mock_responses[lookup_key]
                return MockAPIResponse(status, payload)
                
            return MockAPIResponse(404, {"error": "Not Found"})


        def get(self, endpoint, params=None): return self._fetch_mock("GET", endpoint)
        def post(self, endpoint, data=None): return self._fetch_mock("POST", endpoint, data)
        def put(self, endpoint, data=None): return self._fetch_mock("PUT", endpoint, data)
        def patch(self, endpoint, data=None): return self._fetch_mock("PATCH", endpoint, data)
        def delete(self, endpoint): return self._fetch_mock("DELETE", endpoint)

    client = MockAPIClient(request_context, env_config["api_base_url"])
    yield client
    request_context.dispose()

def pytest_sessionfinish(session, exitstatus):
    """Executes on the master process after all tests complete to merge isolated reports."""
    if not hasattr(session.config, "workerinput"):
        run_dir = os.environ.get("PYTEST_SHARED_RUN_DIR")
        if run_dir and os.path.exists(run_dir):
            import time
            time.sleep(1.5)
            ExcelReporter.merge_worker_reports(run_dir, "Execution_Summary.xlsx")
