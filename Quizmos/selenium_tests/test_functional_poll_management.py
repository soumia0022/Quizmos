import time

# To skip tests in GitHub Actions (when using headed browser)
import os
from unittest import skipIf

from django.test import TestCase
from selenium.webdriver.common.by import By
from django.shortcuts import reverse

from Quizmos.selenium_tests import log_in, wait, wait_for_clickable, wait_for_element  # From __init__.py
from poll_management.tests.fixtures.create_test_polls import create_default_test_polls
from user_management.tests.fixtures.create_test_users import create_default_test_user
from user_management.models.user_model import User
from poll_management.models.poll_model import Poll
from Quizmos.selenium_tests.selenium_test_base import BaseSeleniumTest


# @skipIf(os.environ.get('GITHUB_ACTIONS') == 'true', 'These tests require a visible browser to run.')
class TestFunctionalPollManagement(TestCase, BaseSeleniumTest):
    """This class tests all poll functionality (excluding question specific functionality)."""
    def setUp(self):
        super().setUp()

        # From fixtures folders in relative apps
        create_default_test_user()
        create_default_test_polls()
        self.lecturer = User.objects.get(role='Lecturer')
        self.poll = Poll.objects.get(pk=1)

        log_in(self.driver, self.live_server_url, self.lecturer.username, 'Password123')
        self.driver.get(f"{self.live_server_url}{reverse('user_management:dashboard')}")
        wait(self.driver)


    def test_user_can_view_poll(self):
        view_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_poll_view_button"))  # From lecturer_dashboard.html
        view_button.click()
        wait(self.driver)
        # time.sleep(1)  # To ensure page stabilises + so I can see what is happening

        view_poll_title_element = wait_for_element(self.driver, By.ID, "id_view_poll_title")  # From view_poll.html
        expected_title = "Results for Poll: Sample Poll"
        self.assertEqual(expected_title, view_poll_title_element.text)


    def test_user_can_edit_poll(self):
        edit_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_poll_edit_button"))
        edit_button.click()
        wait(self.driver)

        edit_poll_title_element = wait_for_element(self.driver, By.ID, "id_edit_poll_title")  # From edit_poll.html
        expected_title = "Edit Poll: Sample Poll"
        self.assertEqual(expected_title, edit_poll_title_element.text)

    # def test_user_can_delete_poll(self):
