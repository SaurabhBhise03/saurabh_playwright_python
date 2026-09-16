from playwright.sync_api import APIRequestContext, APIResponse
from typing import Dict, Any, Optional

class APIClient:
    """
    Isolated wrapper mapping standard HTTP verbs using Playwright's native APIRequestContext.
    Ensures seamless abstract layers away from raw framework context calls.
    """
    def __init__(self, request_context: APIRequestContext, base_url: str):
        self.request_context = request_context
        self.base_url = base_url

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Executes HTTP GET targeting the selected endpoint payload context."""
        return self.request_context.get(f"{self.base_url}{endpoint}", params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Executes HTTP POST targeting the selected endpoint payload context."""
        return self.request_context.post(f"{self.base_url}{endpoint}", data=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Executes HTTP PUT targeting the selected endpoint payload context."""
        return self.request_context.put(f"{self.base_url}{endpoint}", data=data)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Executes HTTP PATCH targeting the selected endpoint payload context."""
        return self.request_context.patch(f"{self.base_url}{endpoint}", data=data)

    def delete(self, endpoint: str) -> APIResponse:
        """Executes HTTP DELETE targeting the selected endpoint payload context."""
        return self.request_context.delete(f"{self.base_url}{endpoint}")
