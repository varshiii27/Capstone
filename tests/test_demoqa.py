"""
DemoQA Full Feature Test Suite
Browsers: Chrome, Edge, Firefox
Features:
1. Radio Button
2. Checkbox
3. Dropdown
4. File Upload
5. Drag & Drop
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from drivers.driver_factory import DriverFactory

# -----------------------------
# Helper: remove floating ads
# -----------------------------
def remove_ads(driver):
    driver.execute_script("""
    var adFrames = document.querySelectorAll('iframe[src*="safeframe"]');
    adFrames.forEach(f => f.style.display='none');
    """)

# -----------------------------
# Fixture for driver setup
# -----------------------------
@pytest.fixture(params=["chrome", "edge", "firefox"])
def setup_driver(request):
    browser_name = request.param
    print(f"\n[Setup] Launching {browser_name.upper()} browser")
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=False)
    driver.maximize_window()
    yield driver, browser_name
    print(f"[Teardown] Closing {browser_name.upper()} browser")
    driver.quit()

# ======================================================================
# TEST 5: RADIO BUTTON
# ======================================================================
@pytest.mark.order(5)
def test_radio_buttons(setup_driver):
    driver, browser_name = setup_driver
    print(f"\n=== TEST: Radio Button on {browser_name.upper()} ===")

    driver.get("https://demoqa.com/radio-button")
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

    yes_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='yesRadio']")))
    driver.execute_script("arguments[0].click();", yes_radio)
    result = driver.find_element(By.CLASS_NAME, "text-success").text
    assert "Yes" in result
    print(f"✅ Selected: {result}")

    impressive_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='impressiveRadio']")))
    driver.execute_script("arguments[0].click();", impressive_radio)
    result = driver.find_element(By.CLASS_NAME, "text-success").text
    assert "Impressive" in result
    print(f"✅ Selected: {result}")

    no_radio = driver.find_element(By.ID, "noRadio")
    assert not no_radio.is_enabled(), "'No' should be disabled"
    print("✅ 'No' radio is disabled")

# ======================================================================
# TEST 6: CHECKBOX
# ======================================================================
@pytest.mark.order(6)
def test_checkboxes(setup_driver):
    driver, browser_name = setup_driver
    print(f"\n=== TEST: Checkbox on {browser_name.upper()} ===")

    driver.get("https://demoqa.com/checkbox")
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)

    expand = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Expand all']")))
    driver.execute_script("arguments[0].click();", expand)

    desktop = driver.find_element(By.XPATH, "//label[@for='tree-node-desktop']/span[@class='rct-checkbox']")
    driver.execute_script("arguments[0].click();", desktop)
    time.sleep(1)

    result = driver.find_element(By.ID, "result").text
    assert "desktop" in result.lower()
    print(f"✅ Selected: {result}")

# ======================================================================
# TEST 7: DROPDOWN
# ======================================================================
@pytest.mark.order(7)
def test_dropdowns(setup_driver):
    driver, browser_name = setup_driver
    print(f"\n=== TEST: Dropdown on {browser_name.upper()} ===")

    driver.get("https://demoqa.com/select-menu")
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)

    old_select = wait.until(EC.visibility_of_element_located((By.ID, "oldSelectMenu")))
    select_obj = Select(old_select)
    select_obj.select_by_visible_text("Purple")
    print(f"✅ Selected: {select_obj.first_selected_option.text}")

    multi_select = driver.find_element(By.ID, "cars")
    multi_select_obj = Select(multi_select)
    if multi_select_obj.is_multiple:
        multi_select_obj.select_by_visible_text("Volvo")
        multi_select_obj.select_by_visible_text("Audi")
        selected = [o.text for o in multi_select_obj.all_selected_options]
        print(f"✅ Multi-selected: {selected}")
        multi_select_obj.deselect_all()
        print("✅ Deselected all")

# ======================================================================
# TEST 8: FILE UPLOAD
# ======================================================================
@pytest.mark.order(8)
def test_file_upload(setup_driver):
    driver, browser_name = setup_driver
    print(f"\n=== TEST: File Upload on {browser_name.upper()} ===")

    driver.get("https://demoqa.com/upload-download")
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)

    # 🔧 Make sure this file path exists on your system
    test_file = r"C:\Users\Ascendion\OneDrive\Documents\sql.txt"

    upload_input = wait.until(EC.presence_of_element_located((By.ID, "uploadFile")))
    upload_input.send_keys(test_file)
    time.sleep(2)

    uploaded_path = driver.find_element(By.ID, "uploadedFilePath").text
    assert "sql.txt" in uploaded_path
    print(f"✅ File uploaded: {uploaded_path}")

# ======================================================================
# TEST 9: DRAG & DROP
# ======================================================================
@pytest.mark.order(9)
def test_drag_drop_demo(setup_driver):
    driver, browser_name = setup_driver
    print(f"\n=== TEST: Drag and Drop on {browser_name.upper()} ===")

    driver.get("https://demoqa.com/droppable")
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)

    actions = ActionChains(driver)
    source = wait.until(EC.visibility_of_element_located((By.ID, "draggable")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "droppable")))

    actions.drag_and_drop(source, target).perform()
    time.sleep(2)

    target_text = target.text
    assert "Dropped!" in target_text
    print(f"✅ Target text after drop: {target_text}")
