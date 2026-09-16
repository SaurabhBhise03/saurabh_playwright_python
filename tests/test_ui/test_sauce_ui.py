import os
import pytest
import time
from page_objects.pages.login_page import LoginPage
from page_objects.pages.inventory_page import InventoryPage
from utils.data_reader import DataReader
from playwright.sync_api import sync_playwright

@pytest.mark.ui
class TestSauceUiAutomation:
    """
    Production-grade enterprise UI automation test suite evaluating 10 comprehensive 
    user workflows on SauceDemo. Synchronizes step details directly into embedded Excel reports.
    """

    # 1. DATA DRIVEN MULTI INPUT TESTING MATRIX
    def test_login_matrix(self, page, execution_context, excel_logger, env_config, request):
        """Processes invalid and structured edge case scenarios through parameterized matrix arrays."""
        test_name = request.node.name
        data = DataReader.get_ui_data("test_login_matrix")
        login_view = LoginPage(page, execution_context, test_name=test_name)
        
        for index, scenario in enumerate(data["scenarios"]):
            start_time = time.time()
            login_view.navigate_to(env_config["ui_base_url"])
            img_login = login_view.execute_login(scenario["username"], scenario["password"])
            
            error_msg = login_view.get_error_message()
            assert error_msg == scenario["expected_error"]
            
            duration = time.time() - start_time
            excel_logger.append_step_result(
                test_name=f"{test_name}_Scenario_{index+1}",
                step_desc=f"Validated credentials for user [{scenario['username']}]",
                status="PASSED",
                duration=duration,
                screenshot_path=img_login
            )

    # 2. STATE GENERATION AND AUTH STORAGE TEST
    @pytest.mark.auth
    def test_generate_auth_state(self, page, execution_context, excel_logger, env_config, request):
        """Validates successful entry and flushes session cache state profiles directly onto storage disk spaces."""
        test_name = request.node.name
        start_time = time.time()
        
        login_view = LoginPage(page, execution_context, test_name=test_name)
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        
        login_view.navigate_to(env_config["ui_base_url"])
        login_view.execute_login("standard_user", "secret_sauce")
        img_dash = inventory_view.verify_on_inventory_page()
        
        state_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "state")
        os.makedirs(state_dir, exist_ok=True)
        state_path = os.path.join(state_dir, "auth_state.json")
        page.context.storage_state(path=state_path)
        
        assert os.path.exists(state_path)
        
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Authenticate standard_user and preserve auth_state.json context", "PASSED", duration, img_dash)

    # 3. REUSING CAPTURED AUTHENTICATION STATE BYPASSING LOGIN GATEWAY
    @pytest.mark.auth
    def test_consume_auth_state(self, browser, execution_context, excel_logger, env_config, request):
        """Injects saved storage contexts enabling scripts to execute inside inner pages directly."""
        test_name = request.node.name
        start_time = time.time()
        
        state_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "state", "auth_state.json")
        if not os.path.exists(state_path):
            pytest.skip("Skipping consumer verification: Required auth_state.json not compiled on disk.")
            
        context = browser.new_context(storage_state=state_path)
        page = context.new_page()
        
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        inventory_view.navigate_to(f"{env_config['ui_base_url']}/inventory.html")
        img_dash = inventory_view.verify_on_inventory_page()
        
        context.close()
        
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Bypass authentication layout using stored token profiles", "PASSED", duration, img_dash)

    # 4. ITEM SELECTION & BASKET INTERACTION MODES
    def test_add_to_cart(self, page, execution_context, excel_logger, env_config, request):
        """Ensures selecting operational elements scales internal product shopping badge counters."""
        test_name = request.node.name
        start_time = time.time()
        
        login_view = LoginPage(page, execution_context, test_name=test_name)
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        
        login_view.navigate_to(env_config["ui_base_url"])
        login_view.execute_login("standard_user", "secret_sauce")
        img_add = inventory_view.add_first_product_to_cart()
        
        assert inventory_view.get_cart_badge_count() == "1"
        
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Verify item addition correctly populates checkout container metrics", "PASSED", duration, img_add)

    # 5. REMOVE ITEM FROM CART BASKET
    def test_remove_from_cart(self, page, execution_context, excel_logger, env_config, request):
        """Ensures removal actions accurately reverse cart badge numeric counts."""
        test_name = request.node.name
        start_time = time.time()
        
        login_view = LoginPage(page, execution_context, test_name=test_name)
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        
        login_view.navigate_to(env_config["ui_base_url"])
        login_view.execute_login("standard_user", "secret_sauce")
        inventory_view.add_first_product_to_cart()
        
        page.locator("button[data-test^='remove']").first.click()
        img_remove = inventory_view.capture_step_screenshot("Item Cleared From Basket")
        
        assert page.locator(".shopping_cart_badge").count() == 0
        
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Verify removing selection drops badge metric elements cleanly", "PASSED", duration, img_remove)

    # 6. CATALOGUE FILTERING & SORTING ITERATIONS: A TO Z
    def test_sorting_az(self, page, execution_context, excel_logger, env_config, request):
        """Verifies operational order transitions evaluating alphabetical option triggers."""
        test_name = request.node.name
        start_time = time.time()
        
        login_view = LoginPage(page, execution_context, test_name=test_name)
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        
        login_view.navigate_to(env_config["ui_base_url"])
        login_view.execute_login("standard_user", "secret_sauce")
        img_sort = inventory_view.change_sorting("az")
        
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Verify Catalog Order Sequence: Name A to Z", "PASSED", duration, img_sort)

    # 7. CATALOGUE FILTERING & SORTING ITERATIONS: Z TO A
    def test_sorting_za(self, page, execution_context, excel_logger, env_config, request):
        """Verifies operational order transitions evaluating reverse-alphabetical option triggers."""
        test_name = request.node.name
        start_time = time.time()
        
        login_view = LoginPage(page, execution_context, test_name=test_name)
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        
        login_view.navigate_to(env_config["ui_base_url"])
        login_view.execute_login("standard_user", "secret_sauce")
        img_sort = inventory_view.change_sorting("za")
        
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Verify Catalog Order Sequence: Name Z to A", "PASSED", duration, img_sort)

    # 8. CATALOGUE FILTERING & SORTING ITERATIONS: LOW TO HIGH
    def test_sorting_lohi(self, page, execution_context, excel_logger, env_config, request):
        """Verifies operational order transitions evaluating cost ascending option triggers."""
        test_name = request.node.name
        start_time = time.time()
        
        login_view = LoginPage(page, execution_context, test_name=test_name)
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        
        login_view.navigate_to(env_config["ui_base_url"])
        login_view.execute_login("standard_user", "secret_sauce")
        img_sort = inventory_view.change_sorting("lohi")
        
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Verify Catalog Order Sequence: Price Low to High", "PASSED", duration, img_sort)

    # 9. CATALOGUE FILTERING & SORTING ITERATIONS: HIGH TO LOW
    def test_sorting_hilo(self, page, execution_context, excel_logger, env_config, request):
        """Verifies operational order transitions evaluating cost descending option triggers."""
        test_name = request.node.name
        start_time = time.time()
        
        login_view = LoginPage(page, execution_context, test_name=test_name)
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        
        login_view.navigate_to(env_config["ui_base_url"])
        login_view.execute_login("standard_user", "secret_sauce")
        img_sort = inventory_view.change_sorting("hilo")
        
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Verify Catalog Order Sequence: Price High to Low", "PASSED", duration, img_sort)

    # 10. DISMISSAL & NAVIGATION TRACKING SCENARIOS
    def test_sidebar_logout(self, page, execution_context, excel_logger, env_config, request):
        """Proves secure session teardown redirects endpoints back to authentication home roots."""
        test_name = request.node.name
        start_time = time.time()
        login_view = LoginPage(page, execution_context, test_name=test_name)
        inventory_view = InventoryPage(page, execution_context, test_name=test_name)
        login_view.navigate_to(env_config["ui_base_url"])
        login_view.execute_login("standard_user", "secret_sauce")
        img_out = inventory_view.execute_logout()
        assert page.url == f"{env_config['ui_base_url']}/"
        duration = time.time() - start_time
        excel_logger.append_step_result(test_name, "Verify session clear triggers redirection back to home", "PASSED", duration, img_out)