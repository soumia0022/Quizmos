from django.test import TestCase
from selenium.webdriver.common.by import By
from django.shortcuts import reverse

from Quizmos.selenium_tests import log_in, wait, wait_for_clickable, wait_for_element  # From __init__.py
from poll_management.tests.fixtures.create_test_polls import create_default_test_polls
from user_management.tests.fixtures.create_test_users import create_default_test_user
from user_management.models.user_model import User
from poll_management.models.poll_model import Poll
from Quizmos.selenium_tests.selenium_test_base import BaseSeleniumTest

# Write tests for create poll once functionality has been changed/fixed
# Can add test to view the questions list of all questions in the poll tha comes up on the side once it is confirmed
# that the code for it will not change

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

    def tearDown(self):
        super().tearDown()

    def test_user_can_view_poll(self):
        view_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_poll_view_button"))  # From lecturer_dashboard.html
        view_button.click()
        wait(self.driver)
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

    def test_user_can_delete_poll(self):
        delete_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "id_poll_delete_button"))
        delete_button.click()

        wait_for_element(self.driver, By.ID, "custom-popup")  # In lecturer_dashboard.html

        # Wait for the "Yes" button and click to confirm deletion
        confirm_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "confirm-delete"))  # Already given ID by another group member
        confirm_button.click()
        wait(self.driver)

        self.assertFalse(Poll.objects.filter(pk=self.poll.id).exists(), "Poll was not deleted!")

    def test_user_can_see_poll_start_page_and_start_poll(self):
        start_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "id_poll_start_button"))
        start_button.click()
        wait(self.driver)

        start_poll_title_element = wait_for_element(self.driver, By.ID, "id_start_poll_title")  # From display_code.html
        expected_title = "Sample Poll"
        self.assertEqual(expected_title, start_poll_title_element.text)

        start_poll_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "start-poll-btn"))  # Already given ID by another group member
        start_poll_button.click()
        wait(self.driver)

        prev_button = wait_for_element(self.driver, By.ID, "prev-btn")  # ID already given
        next_button = wait_for_element(self.driver, By.ID, "next-btn")  # ID already given
        self.assertTrue(prev_button.is_displayed(), "'Prev' button is not visible!")
        self.assertTrue(next_button.is_displayed(), "'Next' button is not visible!")
