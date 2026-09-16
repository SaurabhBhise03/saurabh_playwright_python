from page_objects.pages.base_page import BasePage
from page_objects.locators.login_locators import LoginLocators
from playwright.sync_api import Page

class LoginPage(BasePage):
    """Orchestrates structural operational user movements targeting credentials validation gateways."""
    def __init__(self, page: Page, report_dir: str, test_name: str = "Unhandled_Test"):
        # Explicitly forward the test name context down to the BasePage framework layer
        super().__init__(page, report_dir, test_name)

    def execute_login(self, username: str, password: str) -> str:
        """
        Performs structured UI input interactions utilizing explicit wait verification checks.
        Returns the path of the captured screenshot taken immediately post-credentials submission.
        """
        self.page.wait_for_selector(LoginLocators.USERNAME_INPUT, state="visible")
        self.page.fill(LoginLocators.USERNAME_INPUT, username)
        self.page.fill(LoginLocators.PASSWORD_INPUT, password)
        self.page.click(LoginLocators.LOGIN_BUTTON)
        # Capture screenshot post-click and return file path for reporting
        return self.capture_step_screenshot("Submitted Login Form")

    def get_error_message(self) -> str:
        """Extracts validation messages surfaced cleanly upon encountering processing exceptions."""
        self.page.wait_for_selector(LoginLocators.ERROR_CONTAINER, state="visible")
        return self.page.locator(LoginLocators.ERROR_CONTAINER).inner_text()
