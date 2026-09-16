from page_objects.pages.base_page import BasePage
from page_objects.locators.inventory_locators import InventoryLocators
from playwright.sync_api import Page, expect

class InventoryPage(BasePage):
    """Orchestrates comprehensive interface validation functions operating inside product catalog dashboards."""
    def __init__(self, page: Page, report_dir: str, test_name: str = "Unhandled_Test"):
        # Explicitly forward the test name context down to the BasePage framework layer
        super().__init__(page, report_dir, test_name)

    def verify_on_inventory_page(self) -> str:
        """
        Validates that authenticated landing indicators possess explicit functional rendering.
        Returns screenshot proof path string.
        """
        self.page.wait_for_selector(InventoryLocators.INVENTORY_CONTAINER, state="visible")
        expect(self.page.locator(InventoryLocators.HEADER_TITLE)).to_have_text("Products")
        return self.capture_step_screenshot("Verified Inventory Dashboard Dashboard")

    def add_first_product_to_cart(self) -> str:
        """Interacts with item matrices to cleanly execute addition commands."""
        self.page.wait_for_selector(InventoryLocators.ADD_TO_CART_BTN, state="visible")
        self.page.locator(InventoryLocators.ADD_TO_CART_BTN).first.click()
        return self.capture_step_screenshot("Added Item To Cart Basket")

    def get_cart_badge_count(self) -> str:
        """Retrieves textual representations denoting tracking item quantities currently selected."""
        self.page.wait_for_selector(InventoryLocators.CART_BADGE, state="visible")
        return self.page.locator(InventoryLocators.CART_BADGE).inner_text()

    def change_sorting(self, option_value: str) -> str:
        """Alters target display sequences using core system selector options."""
        self.page.wait_for_selector(InventoryLocators.SORT_DROPDOWN, state="visible")
        self.page.select_option(InventoryLocators.SORT_DROPDOWN, value=option_value)
        return self.capture_step_screenshot(f"Sorting Changed To {option_value}")

    def execute_logout(self) -> str:
        """Triggers system logging extraction paths via responsive control widgets."""
        self.page.click(InventoryLocators.SIDEBAR_BURGER_MENU)
        self.page.wait_for_selector(InventoryLocators.LOGOUT_SIDEBAR_LINK, state="visible")
        self.page.click(InventoryLocators.LOGOUT_SIDEBAR_LINK)
        return self.capture_step_screenshot("Executed Session Logout")
