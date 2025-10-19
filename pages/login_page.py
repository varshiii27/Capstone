from selenium.webdriver.common.by import By
from utilities.wait_utils import WaitUtils

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.login_button_nav = (By.ID, "login2")           # top nav "Log in"
        self.username_input = (By.ID, "loginusername")     # modal username
        self.password_input = (By.ID, "loginpassword")     # modal password
        self.submit_button = (By.XPATH, "//button[text()='Log in']")  # modal submit

    def open_login_modal(self):
        WaitUtils.wait_for_element_clickable(self.driver, self.login_button_nav).click()

    def enter_username(self, username):
        WaitUtils.wait_for_element_visible(self.driver, self.username_input).clear()
        WaitUtils.wait_for_element_visible(self.driver, self.username_input).send_keys(username)

    def enter_password(self, password):
        WaitUtils.wait_for_element_visible(self.driver, self.password_input).clear()
        WaitUtils.wait_for_element_visible(self.driver, self.password_input).send_keys(password)

    def click_login(self):
        WaitUtils.wait_for_element_clickable(self.driver, self.submit_button).click()
