import os
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utilits.driver_factory import get_driver
from utilits.POM_helper_class import MainPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:3000')  # Default to localhost if not set

class ExampleTestCase(unittest.TestCase):
    
    
    def setUp(self):
        self.driver = get_driver()
        self.driver.implicitly_wait(10)
        self.page = MainPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_page_title(self):
        self.page.go_to(OLLAMA_URL)
        self.assertIn('Ollama UI', self.driver.title)
    
    def test_send_message(self):#TODO: need to update the test to handle the new driver factory change the code to pom 
        self.driver.get(OLLAMA_URL)
        dropdown=self.driver.find_element(By.CSS_SELECTOR,"button[role='combobox']")
        dropdown.click()
        gemma3 = self.driver.find_element(By.XPATH, "//*[text()='gemma3:1b']")
        gemma3.click()
        time.sleep(1)
        button = self.driver.find_element(By.NAME, "message")
        button.click()
        button.send_keys("Hello! Can you help me with Python?")
        button1 = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button1.click()
        time.sleep(1)
        textarea = self.driver.find_element(By.NAME, "message")
        self.assertEqual(textarea.text,'')

    def test_send_message(self):
        self.page.go_to(OLLAMA_URL)
        self.page.select_model("gemma3:1b")
        self.page.send_message("Hello! Can you help me with Python?")
        self.assertEqual(self.page.get_message_box_text(), '')
        self.assertTrue(self.page.is_response_displayed())

    def test_change_name(self):
        self.page.go_to(OLLAMA_URL)
        changed = self.page.change_name("hamad")
        self.assertEqual(changed, "hamad")
if __name__ == '__main__':
    unittest.main()