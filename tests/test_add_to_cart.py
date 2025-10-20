import pytest
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from drivers.driver_factory import DriverFactory
from pages.product_page import ProductPage

@pytest.mark.order(3)
@pytest.mark.parametrize("browser_name", ["chrome", "edge", "firefox"])
def test_add_to_cart(browser_name):
    print("\n=== Starting Add to Cart Test ===")
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=True)
    driver.get("https://www.demoblaze.com")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    product_page = ProductPage(driver)
    print("[Step] Opening a product...")
    product_page.open_product()
    time.sleep(1)

    # 🔹 FEATURE 1: Scroll down (JavaScript Executor)
    driver.execute_script("window.scrollBy(0, 500);")
    print("[Feature] Scrolled down 500px.")
    time.sleep(1)

    # 🔹 FEATURE 2: Handling multiple WebElements
    items = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
    print(f"[Feature] Total products listed: {len(items)}")
    for i, item in enumerate(items[:5], start=1):  # show only first 5
        print(f"  Product {i}: {item.text}")

    # 🔹 FEATURE 3: Add to Cart and handle Alert
    print("[Feature] Adding product to cart...")
    product_page.add_to_cart()
    try:
        alert = wait.until(EC.alert_is_present())
        print(f"[Alert] Alert text: {alert.text}")
        alert.accept()
        print("[Alert] Alert accepted successfully.")
    except:
        print("[Alert] No alert appeared.")

    # 🔹 FEATURE 4: Drag & Drop Simulation
    try:
        logo = driver.find_element(By.XPATH, "//a[@id='nava']")
        actions.drag_and_drop_by_offset(logo, 20, 0).perform()
        print("[Feature] Drag action performed on logo.")
    except Exception as e:
        print("[Feature] Drag simulation skipped:", e)

    # 🔹 FEATURE 5: Right Click (context click)
    try:
        actions.context_click(logo).perform()
        print("[Feature] Right-click action performed on logo.")
    except Exception as e:
        print("[Feature] Right-click failed:", e)

    # 🔹 FEATURE 6: Window Handling
    print("[Feature] Opening new window and switching...")
    main_window = driver.current_window_handle
    driver.execute_script("window.open('https://www.demoblaze.com/about.html', '_blank');")
    time.sleep(2)
    all_windows = driver.window_handles
    for win in all_windows:
        if win != main_window:
            driver.switch_to.window(win)
            print("[Window Handling] Switched to About Us page.")
            time.sleep(1)
            driver.close()
            print("[Window Handling] Closed About Us page window.")
            break
    driver.switch_to.window(main_window)
    print("[Window Handling] Back to main window.")

    # 🔹 FEATURE 7: Wait for Cart Link & Navigate
    cart_link = wait.until(EC.element_to_be_clickable((By.ID, "cartur")))
    cart_link.click()
    print("[Feature] Navigated to Cart page.")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("[Feature] Scrolled to bottom of cart page.")

    print("✅ Add to Cart test executed with all advanced Selenium features.")
    driver.quit()
    print("=== Test Completed ===\n")
