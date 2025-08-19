
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import time



class MainPage:
	MODEL_DROPDOWN = (By.CSS_SELECTOR, "button[role='combobox']")
	MESSAGE_BOX = (By.NAME, "message")
	SEND_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
	RESPONSE = (By.CSS_SELECTOR, ".p-4.bg-secondary.text-secondary-foreground.rounded-r-lg.rounded-tl-lg.break-words.max-w-full.whitespace-pre-wrap")
	PROFILE_BUTTON = (By.ID, "radix-:Rln7mjt6:")  # Adjust this ID based on your actual application this might change
	# PROFILE_BUTTON = (By.ID, "radix-:Rln7mjt6:")  # Adjust this ID based on your actual application --- IGNORE ---

	side_bar_menu = (By.CSS_SELECTOR, 'button[aria-haspopup="dialog"]')
	mobile_button = (By.XPATH, "//div[@data-collapsed='false']//div//button[@type='button']")#this is for the button for showing the settings menu on mobile
	
	name_check = lambda self,new_name: (By.XPATH, f"//div[@data-collapsed='false']//div//button[@type='button']//div//p[contains(text(),'{new_name}')]")
	SETTINGS_BUTTON = (By.XPATH, "//div[contains(text(),'Settings')]")
	NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter your name']")
	CHANGE_NAME_BUTTON = (By.XPATH, "//button[normalize-space()='Change name']")
	
	
	def __init__(self, driver):
		self.driver = driver
		self.driver.implicitly_wait(2)
		# Optionally validate page load by title or element
		# if "Ollama UI" not in self.driver.title:
		#     raise Exception("Main page not loaded successfully")

	def go_to(self, url):
		self.driver.get(url)

	def select_model(self, model_name="gemma3:1b"):
		self.driver.find_element(*self.MODEL_DROPDOWN).click()
		self.driver.find_element(By.XPATH, f"//*[text()='{model_name}']").click()

	def send_message(self, message):
		box = self.driver.find_element(*self.MESSAGE_BOX)
		box.click()
		box.send_keys(message)
		self.driver.find_element(*self.SEND_BUTTON).click()

	def get_message_box_text(self):
		return self.driver.find_element(*self.MESSAGE_BOX).text

	def is_response_displayed(self):
		return self.driver.find_element(*self.RESPONSE).is_displayed()

	def change_name(self, new_name):
		width = self.driver.get_window_size()["width"]
		viewport_width = self.driver.execute_script("return window.innerWidth")
		print(f"Viewport width: {viewport_width}")
		print(f"Current window width: {width}")
		
		is_mobile = width <= 500
		if is_mobile:
			self.driver.find_element(*self.side_bar_menu).click()
			self.driver.find_element(*self.mobile_button).click()
		else:
			self.driver.find_element(*self.PROFILE_BUTTON).click()
			profile_button_clicked = self.driver.find_element(*self.PROFILE_BUTTON)
			assert profile_button_clicked.get_attribute("aria-expanded") == "true"
		self.driver.find_element(*self.SETTINGS_BUTTON).click()
		name_input = self.driver.find_element(*self.NAME_INPUT)
		# For Mac: Keys.COMMAND, for Windows/Linux: Keys.CONTROL
		name_input.send_keys(Keys.CONTROL + "a")
		name_input.send_keys(Keys.DELETE)
		name_input.send_keys(new_name)
		self.driver.find_element(*self.CHANGE_NAME_BUTTON).click()
		from selenium.webdriver.support.ui import WebDriverWait
		from selenium.webdriver.support import expected_conditions as EC
		if is_mobile:
			self.driver.find_element(*self.side_bar_menu).click()
			WebDriverWait(self.driver, 20).until(
				EC.text_to_be_present_in_element(self.name_check(new_name), new_name)
			)
			return self.driver.find_element(*self.name_check(new_name)).text

		else:
			WebDriverWait(self.driver, 20).until(
				EC.text_to_be_present_in_element((By.XPATH, f"//p[normalize-space()='{new_name}']"), new_name)
			)
		return self.driver.find_element(By.XPATH, f"//p[normalize-space()='{new_name}']").text
	
# class MainPageforPhone(MainPage):
#     def select_model(self, model_name="gemma3:1b"):
#         dropdown = self.driver.find_element(By.CSS_SELECTOR, "button[role='combobox']")
#         dropdown.click()
#         model = self.driver.find_element(By.XPATH, f"//*[text()='{model_name}']")
#         model.click()
#         self.driver.implicitly_wait(2)