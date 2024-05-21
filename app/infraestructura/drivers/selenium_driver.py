from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from app.config import is_view_chrome_headless


class SeleniumDriver:
    driver = None

    @classmethod
    def init_driver(cls):
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.61 Safari/537.36")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        if is_view_chrome_headless:
            options.add_argument("--headless")

        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    @classmethod
    def get_driver(cls):
        """
        Returns the Selenium driver instance.

        This class method checks if the driver instance is already initialized. If not, it initializes it by calling the `init_driver` method.

        Returns:
            The Selenium driver instance.
        """
        if cls.driver is None:
            cls.init_driver()
        return cls.driver
