from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class BaseDriver:
    driver = None  # Class attribute to store the driver instance

    def __init__(self, context):
        if not BaseDriver.driver:  # Check if driver instance already exists
            if context['browser'] == 'chrome':
                options = ChromeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                # if context['headless'] == 'true':
                options.add_argument("--headless")
                BaseDriver.driver = webdriver.Chrome(options)

            elif context['browser'] == 'firefox':
                options = FirefoxOptions()
                if context['headless'] == 'true':
                    options.add_argument("--headless")
                BaseDriver.driver = webdriver.Firefox(options)

            BaseDriver.driver.maximize_window()
            BaseDriver.driver.implicitly_wait(30)

        self.driver = BaseDriver.driver  # Assign the shared driver instance to self.driver

    def close_browser(self):
        self.driver.quit()
