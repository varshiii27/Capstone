import pytest
import csv
import os
import time
import requests
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage

def ensure_login_data():
    folder = os.path.join(os.getcwd(), "testdata")
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, "login_data.csv")

    if not os.path.exists(file_path):
        with open(file_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["username", "password"])
            writer.writerow(["varshitha reddy", "varshi123"])
    return file_path

def read_login_data():
    file_path = ensure_login_data()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row['username'], row['password']) for row in reader]

@pytest.mark.order(2)
@pytest.mark.parametrize("browser_name", ["chrome", "edge"])
@pytest.mark.parametrize("username,password", read_login_data())
def test_login(browser_name, username, password):
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=True)


    driver.get("https://www.demoblaze.com")
    driver.set_window_size(1920, 1080)
    print("\n=== Starting login test ===")

    # 🔹 FEATURE 1: Broken Links Detection
    print("\n[Feature] Checking for broken links...")
    links = driver.find_elements("tag name", "a")
    print(f"Total links found: {len(links)}")
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith("http"):
            try:
                response = requests.head(href, timeout=5)
                assert response.status_code < 400, f"Broken link detected: {href}"
            except Exception as e:
                print(f"Error checking link: {href} -> {e}")
    print("[Feature] Broken links check completed.")

    # 🔹 FEATURE 2: Navigation Commands
    print("\n[Feature] Testing browser navigation commands...")
    driver.find_element("id", "login2").click()
    print("Clicked on login button.")
    time.sleep(2)
    driver.back()
    print("Navigated back.")
    time.sleep(1)
    driver.forward()
    print("Navigated forward.")
    time.sleep(1)
    driver.refresh()
    print("Refreshed page.")
    print("[Feature] Navigation commands completed.")

    # 🔹 Perform actual login
    print("\n[Action] Performing login...")
    login_page = LoginPage(driver)
    login_page.open_login_modal()
    print("Opened login modal.")
    login_page.enter_username(username)
    print(f"Entered username: {username}")
    login_page.enter_password(password)
    print("Entered password.")
    login_page.click_login()
    print("Clicked login button.")
    time.sleep(3)

    # 🔹 FEATURE 3: Refresh and check user still on homepage
    print("\n[Feature] Checking page after refresh...")
    driver.refresh()
    print("Page refreshed.")
    current_url = driver.current_url
    assert "demoblaze" in current_url, "Unexpected page after refresh."
    print("User is on the expected page after refresh.")

    print(f"\n=== Login test executed successfully for user: {username} ===")
    driver.quit()
