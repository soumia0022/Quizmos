from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import chromedriver_autoinstaller


class BaseSeleniumTest(StaticLiveServerTestCase):
    """Base class for Selenium tests to avoid redundant setup and teardown."""

    def setUp(self):
        chromedriver_autoinstaller.install()

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized") # For full-screen

        # Can remove below lines when wanting to view tests in browser
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

    def tearDown(self):
        self.driver.quit()
