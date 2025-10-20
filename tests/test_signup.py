import pytest
import csv
import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from drivers.driver_factory import DriverFactory
from pages.signup_page import SignupPage

def ensure_signup_data():
    folder = os.path.join(os.getcwd(), "testdata")
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, "signup_data.csv")

    if not os.path.exists(file_path):
        with open(file_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["username", "password"])
            writer.writerow(["varshitha reddy", "varshi123"])
        print(f"Created signup data CSV at: {file_path}")
    else:
        print(f"Using existing signup data CSV at: {file_path}")
    return file_path

def read_signup_data():
    file_path = ensure_signup_data()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [(row['username'], row['password']) for row in reader]
    print(f"Loaded {len(data)} signup data entries from CSV.")
    return data

@pytest.mark.order(1)
@pytest.mark.parametrize("browser_name", ["chrome", "edge", "firefox"])
@pytest.mark.parametrize("username,password", read_signup_data())
def test_signup(browser_name,username, password):
    print(f"\n=== Starting signup test for user: {username} ===")
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=True)
    driver.get("https://www.demoblaze.com")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    # 🔹 FEATURE 1: Mouse Hover (hover over all categories)
    print("\n[Feature] Hovering over all categories...")
    categories = driver.find_elements(By.CSS_SELECTOR, ".list-group-item")
    for cat in categories:
        actions.move_to_element(cat).perform()
        print(f"Hovered over category: {cat.text}")
        time.sleep(0.5)
    print("[Feature] Hovering completed.")

    # 🔹 FEATURE 2: Scroll using JavaScript Executor
    print("\n[Feature] Scrolling page...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Scrolled down")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")
    print("Scrolled up")
    print("[Feature] Scrolling completed.")

    # 🔹 FEATURE 3: Frame (Modal) Handling Simulation
    print("\n[Feature] Opening signup modal...")
    signup_page = SignupPage(driver)
    signup_page.open_signup_modal()
    wait.until(EC.visibility_of_element_located((By.ID, "signInModal")))
    print("Signup modal is visible.")

    # Enter signup details
    print(f"[Action] Entering signup details for user: {username}")
    signup_page.enter_signup_details(username, password)
    signup_page.submit_signup()
    print("Signup submitted. Waiting for potential alert...")
    time.sleep(3)

    # Handle alert popup if shown
    try:
        alert = wait.until(EC.alert_is_present())
        print("Alert message received:", alert.text)
        alert.accept()
        print("Alert accepted.")
    except:
        print("No alert appeared after signup.")

    # 🔹 FEATURE 4: Screenshot in dedicated folder
    screenshots_folder = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshots_folder, exist_ok=True)
    screenshot_path = os.path.join(screenshots_folder, f"signup_{username.replace(' ', '_')}.png")
    driver.save_screenshot(screenshot_path)
    print(f"[Feature] Screenshot saved at: {screenshot_path}")

    driver.quit()
    print(f"=== Signup test completed for user: {username} ===\n")
