import os
import allure
import time
from playwright.sync_api import Page

class BasePage:
    """
    Foundation abstract Page Layer object orchestrating execution level wait tracking wrappers
    and comprehensive inline screenshot engine injections.
    """
    def __init__(self, page: Page, report_dir: str, test_name: str = "Unhandled_Test"):
        self.page = page
        self.report_dir = report_dir
        self.test_name = test_name
        self.screenshot_counter = 0

    def navigate_to(self, url: str) -> str:
        """Navigates target page to designated endpoint and enforces structural load completion checks."""
        start_time = time.time()
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        duration = time.time() - start_time
        img_path = self.capture_step_screenshot("Navigated To URL")
        return img_path

    def capture_step_screenshot(self, step_description: str) -> str:
        """
        Generates contextual verification capture storing elements explicitly into report structures.
        Returns the absolute filepath string to pass to the excel reporter.
        """
        self.screenshot_counter += 1
        clean_desc = step_description.replace(' ', '_').replace(':', '_')
        safe_name = f"{self.test_name}_Step{self.screenshot_counter:02d}_{clean_desc}.png"
        target_folder = os.path.join(self.report_dir, "screenshots")
        os.makedirs(target_folder, exist_ok=True)
        
        path_to_save = os.path.join(target_folder, safe_name)
        self.page.screenshot(path=path_to_save)
        
        # Attach capture metadata continuously into Allure pipeline engine matrixes
        allure.attach.file(path_to_save, name=safe_name, attachment_type=allure.attachment_type.PNG)
        return path_to_save
