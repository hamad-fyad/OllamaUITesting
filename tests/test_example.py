import os
import unittest
import sys
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utilits.driver_factory import get_driver
from utilits.POM_helper_class import MainPage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:3000')  # Default to localhost if not set


@allure.epic("Ollama UI Automation")
@allure.feature("UI Functional Tests")
class ExampleTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.driver.implicitly_wait(10)
        self.page = MainPage(self.driver)

    def tearDown(self):
        if sys.exc_info()[0]:  # If test failed, attach screenshot & page source
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                self.driver.page_source,
                name="Page Source",
                attachment_type=allure.attachment_type.HTML
            )
        self.driver.quit()

    @allure.title("Verify Ollama UI Page Title")
    @allure.description("This test verifies that the Ollama UI homepage title contains 'Ollama UI'.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "ui")
    def test_page_title(self):
        with allure.step("Navigate to Ollama UI"):
            self.page.go_to(OLLAMA_URL)

        with allure.step("Verify page title contains 'Ollama UI'"):
            assert "Ollama UI" in self.driver.title

    @allure.title("Send Message and Verify Response")
    @allure.description("This test sends a message to the chat and validates that a response is displayed.")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("chat", "regression")
    def test_send_message(self):
        with allure.step("Navigate to Ollama UI"):
            self.page.go_to(OLLAMA_URL)

        with allure.step("Send a message to the chat box"):
            self.page.send_message("Hello! Can you help me with Python?")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="After Message Sent",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Verify response is displayed"):
            assert self.page.is_response_displayed()

    @allure.title("Change User Name")
    @allure.description("This test changes the user name and verifies the update is reflected.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "settings")
    def test_change_name(self):
        with allure.step("Navigate to Ollama UI"):
            self.page.go_to(OLLAMA_URL)

        with allure.step("Change user name to 'hamad'"):
            changed = self.page.change_name("hamad")
            allure.attach(
                f"Changed name: {changed}",
                name="Changed Name",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify name was updated"):
            assert changed == "hamad"


if __name__ == '__main__':
    unittest.main()
