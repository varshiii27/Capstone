from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

class DriverFactory:

    @staticmethod
    def get_driver(browser_name="chrome", headless=False):  # <-- add headless
        browser_name = browser_name.lower()
        driver = None

        if browser_name == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            if headless:
                options.add_argument("--headless=new")  # Chrome headless
            driver = webdriver.Chrome(options=options)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.add_argument("--start-maximized")
            if headless:
                options.add_argument("--headless")  # Firefox headless
            driver = webdriver.Firefox(options=options)

        elif browser_name == "edge":
            options = EdgeOptions()
            options.add_argument("--start-maximized")
            if headless:
                options.add_argument("--headless=new")  # Edge headless
            driver = webdriver.Edge(options=options)

        else:
            raise Exception(f"Browser {browser_name} not supported")

        driver.implicitly_wait(10)
        return driver
