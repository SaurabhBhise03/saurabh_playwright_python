import pytest
import time
from utils.data_reader import DataReader

@pytest.mark.api
class TestReqResApiAutomation:
    """Validates 10 robust API verification tests using transparent conftest mock routing layers."""

    def test_get_users(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        response = api_handler.get("/api/users?page=2")
        assert response.status == 200
        assert "data" in response.json()
        excel_logger.append_step_result(test_name, "GET /api/users?page=2 status 200 validation", "PASSED", time.time() - start)

    def test_get_single_user(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        response = api_handler.get("/api/users/2")
        assert response.status == 200
        assert response.json()["data"]["id"] == 2
        excel_logger.append_step_result(test_name, "GET /api/users/2 matching ID check", "PASSED", time.time() - start)

    def test_user_not_found(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        response = api_handler.get("/api/users/23")
        assert response.status == 404
        excel_logger.append_step_result(test_name, "GET non-existent user returns 404", "PASSED", time.time() - start)

    def test_create_user(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        payload = DataReader.get_api_data("test_create_user")
        response = api_handler.post("/api/users", data=payload)
        assert response.status == 201
        assert response.json()["name"] == payload["name"]
        excel_logger.append_step_result(test_name, "POST /api/users creation record verify", "PASSED", time.time() - start)

    def test_update_user_put(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        payload = {"name": "morpheus", "job": "zion resident"}
        response = api_handler.put("/api/users/2", data=payload)
        assert response.status == 200
        assert response.json()["job"] == payload["job"]
        excel_logger.append_step_result(test_name, "PUT full modification mapping", "PASSED", time.time() - start)

    def test_update_user_patch(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        payload = {"job": "architect"}
        response = api_handler.patch("/api/users/2", data=payload)
        assert response.status == 200
        assert response.json()["job"] == payload["job"]
        excel_logger.append_step_result(test_name, "PATCH partial alteration metadata verification", "PASSED", time.time() - start)

    def test_delete_user(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        response = api_handler.delete("/api/users/2")
        assert response.status == 204
        excel_logger.append_step_result(test_name, "DELETE user context payload erasure signature", "PASSED", time.time() - start)

    def test_register_success(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
        response = api_handler.post("/api/register", data=payload)
        assert response.status == 200
        assert "token" in response.json()
        excel_logger.append_step_result(test_name, "POST successful registration returns token", "PASSED", time.time() - start)

    def test_register_unsuccessful(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        payload = {"email": "sydney@fife"}
        response = api_handler.post("/api/register", data=payload)
        assert response.status == 400
        assert response.json()["error"] == "Missing password"
        excel_logger.append_step_result(test_name, "POST missing fields triggers errors", "PASSED", time.time() - start)

    def test_login_api_success(self, api_handler, excel_logger, request):
        test_name = request.node.name
        start = time.time()
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        response = api_handler.post("/api/login", data=payload)
        assert response.status == 200
        assert "token" in response.json()
        excel_logger.append_step_result(test_name, "POST verification endpoint confirms identity validations", "PASSED", time.time() - start)
