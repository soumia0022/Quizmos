import time
from django.test import TestCase
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from django.shortcuts import reverse
import ast  # To safely convert string to list
from selenium.webdriver.common.action_chains import ActionChains

from Quizmos.selenium_tests import log_in, wait, wait_for_clickable, wait_for_element  # From __init__.py
from poll_management.tests.fixtures.create_test_polls import create_default_test_polls
from user_management.tests.fixtures.create_test_users import create_default_test_user
from user_management.models.user_model import User
from poll_management.models.poll_model import Poll
from Quizmos.selenium_tests.selenium_test_base import BaseSeleniumTest

# Add more tests for go back and return to dashboard buttons (as more of these may be added)

class TestSystemButtons(TestCase, BaseSeleniumTest):
    """This class tests all button functionality (through a user's perspective) - go back buttons and return to
    dashboard buttons."""
    def setUp(self):
        super().setUp()

        # From fixtures folders in relative apps
        create_default_test_user()
        create_default_test_polls()
        self.lecturer = User.objects.get(role='Lecturer')
        self.poll = Poll.objects.get(pk=1)

        log_in(self.driver, self.live_server_url, self.lecturer.username, 'Password123')

    def tearDown(self):
        super().tearDown()

    def test_go_back_button_on_change_profile_page(self):
        self.driver.get(f"{self.live_server_url}{reverse('user_management:profile')}")
        go_back_button = wait_for_element(self.driver, By.ID, "go-back-btn")
        go_back_button.click()  # Leads back to the dashboard so user should be able to see their polls (and so poll start button)
        wait(self.driver)
        start_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "id_poll_start_button"))
        self.assertTrue(start_button.is_displayed(), "'Start' button is not visible!")

    def test_return_to_dashboard_button_on_add_question_page(self):
        # Navigate to add question page from dashboard
        self.driver.get(f"{self.live_server_url}{reverse('user_management:dashboard')}")
        wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_poll_edit_button")).click()
        wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_edit_questions_button")).click()

        return_button = wait_for_element(self.driver, By.ID, "return-to-dash-btn")
        return_button.click()  # Leads back to the dashboard so user should be able to see their polls (and so poll start button)
        wait(self.driver)
        start_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "id_poll_start_button"))
        self.assertTrue(start_button.is_displayed(), "'Start' button is not visible!")

    # Add more button tests here once fully decided which pages the buttons should be on

class TestOtherSystemComponents(TestCase, BaseSeleniumTest):
    """This class tests all other system components functionality that has ot been covered by the other test classes.
    It tests information buttons ... ."""

    def setUp(self):
        super().setUp()

        # From fixtures folders in relative apps
        create_default_test_user()
        create_default_test_polls()
        self.lecturer = User.objects.get(role='Lecturer')
        self.poll = Poll.objects.get(pk=1)

        log_in(self.driver, self.live_server_url, self.lecturer.username, 'Password123')
        wait(self.driver)

    def tearDown(self):
        super().tearDown()

