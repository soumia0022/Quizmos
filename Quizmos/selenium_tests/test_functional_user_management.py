import time

# To skip tests in GitHub Actions (when using headed browser)
import os
from unittest import skipIf

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import reverse

from django.conf import settings
from Quizmos.selenium_tests import log_in, wait, wait_for_clickable, wait_for_element  # From __init__.py
from user_management.tests.fixtures.create_test_users import create_default_test_user  # In fixtures
from user_management.models.user_model import User


# @skipIf(os.environ.get('GITHUB_ACTIONS') == 'true', 'These tests require a visible browser to run.')
class TestFunctionalRegistration(StaticLiveServerTestCase):
    """This class tests user registration functionality."""
    def setUp(self):
        chromedriver_autoinstaller.install()

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")  # Can remove this to see the tests run on the browser
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

    def tearDown(self):
        self.driver.quit()

    def test_user_can_register(self):
        self.driver.get(f"{self.live_server_url}{reverse('user_management:sign_up')}")  # Navigate to signup page
        wait(self.driver)  # Wait for page to load

        # Get and fill out form fields
        fields = self.get_user_form_fields()
        self.fill_out_fields(fields)

        # Ensure the page redirects after form submission
        wait(self.driver)
        self.assertEqual(
            self.driver.current_url,
            f"{self.live_server_url}{reverse(settings.LOGIN_REDIRECT_URL)}"
        )
        # Ensure new user now exists
        self.assertTrue(User.objects.filter(username='charlie').exists())
        charlie = User.objects.get(username='charlie')
        self.assertEqual(charlie.first_name, "Charlie")
        self.assertEqual(charlie.last_name, "Johnson")
        self.assertEqual(charlie.email, "charlie@example.com")
        self.assertEqual(charlie.role, "Lecturer")

    # Helper methods below

    def get_user_form_fields(self):
        """This method waits for the registration form fields to be present in the DOM and then
        returns the form fields as a tuple to be used in the fill_out_fields method."""
        username_input = wait_for_element(self.driver, By.ID, "id_username")
        first_name_input = wait_for_element(self.driver, By.ID, "id_first_name")
        last_name_input = wait_for_element(self.driver, By.ID, "id_last_name")
        email_input = wait_for_element(self.driver, By.ID, "id_email")
        role_input = wait_for_element(self.driver, By.ID, "id_role")
        password_input = wait_for_element(self.driver, By.ID, "id_new_password")
        confirm_password_input = wait_for_element(self.driver, By.ID, "id_password_confirmation")
        submit = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_sign_up_button"))

        return (username_input, first_name_input, last_name_input, email_input, role_input,
                password_input, confirm_password_input, submit)

    def fill_out_fields(self, fields: tuple):
        """This method fills in the fields (using select to choose the role from the dropdown), and then
        submits the form."""
        (username_input, first_name_input, last_name_input, email_input,
         role_input, password_input, confirm_password_input, submit) = fields

        username_input.send_keys("charlie")
        first_name_input.send_keys("Charlie")
        last_name_input.send_keys("Johnson")
        email_input.send_keys("charlie@example.com")
        role = Select(role_input)
        role.select_by_visible_text("Lecturer")
        password_input.send_keys("Password123")
        confirm_password_input.send_keys("Password123")

        # Scroll to submit button to avoid "ElementClickInterceptedException"
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit)
        time.sleep(1)  # Ensure page stabilises before clicking
        try:
            submit.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", submit)

    # End of helper methods


# @skipIf(os.environ.get('GITHUB_ACTIONS') == 'true', 'These tests require a visible browser to run.')
class TestFunctionalUserSystem(StaticLiveServerTestCase):
    """This class tests user login and password change functionality."""
    def setUp(self):
        chromedriver_autoinstaller.install()

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")  # Can remove this to see the tests run on the browser
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

        create_default_test_user()
        self.lecturer = User.objects.get(role='Lecturer')

    def tearDown(self):
        self.driver.quit()

    def test_user_can_log_in(self):
        log_in(self.driver, self.live_server_url, self.lecturer.username, 'Password123')
        wait(self.driver)
        self.assertEqual(self.driver.current_url,
                         f"{self.live_server_url}{reverse(settings.LOGIN_REDIRECT_URL)}")

    def test_attempt_log_in_with_wrong_credentials_does_not_work(self):
        log_in(self.driver, self.live_server_url, self.lecturer.username, 'WrongPassword')
        self.assertNotEqual(self.driver.current_url,
                            f"{self.live_server_url}{reverse(settings.LOGIN_REDIRECT_URL)}")
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}{reverse('user_management:log_in')}")
        self.assertIn("The credentials provided were invalid!", self.driver.page_source)

    def test_user_can_change_their_password(self):
        log_in(self.driver, self.live_server_url, self.lecturer.username, 'Password123')
        self.driver.get(f"{self.live_server_url}{reverse('user_management:password')}")
        wait(self.driver)
        self.populate_password_fields(self.get_password_change_fields())
        wait(self.driver)
        self.lecturer.refresh_from_db()
        self.assertTrue(self.lecturer.check_password("NewPassword123"))  # Verify password has been updated

    # Helper methods below

    def get_password_change_fields(self) -> tuple:
        new_password_input = wait_for_element(self.driver, By.ID, "id_new_password")
        password_confirmation_input = wait_for_element(self.driver, By.ID, "id_password_confirmation")
        current_password_input = wait_for_element(self.driver, By.ID, "id_password")
        submit_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_change_password"))
        return new_password_input, password_confirmation_input, current_password_input, submit_button

    def populate_password_fields(self, fields: tuple):
        new_password_input, password_confirmation_input, current_password_input, submit_button = fields
        new_password_input.send_keys("NewPassword123")
        password_confirmation_input.send_keys("NewPassword123")
        current_password_input.send_keys("Password123")

        # Scroll to submit button to avoid "ElementClickInterceptedException"
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)  # Ensure page stabilises before clicking
        try:
            submit_button.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", submit_button)

    # End of helper methods