from django.test import TestCase
from selenium.webdriver.common.by import By
from django.shortcuts import reverse
import time
from selenium.webdriver.common.action_chains import ActionChains

from Quizmos.selenium_tests import log_in, wait, wait_for_element, wait_for_clickable
from user_management.tests.fixtures.create_test_users import create_default_test_user
from poll_management.tests.fixtures.create_test_polls import create_default_test_polls
from question_management.tests.fixtures.load_fixtures import load_default_questions
from response_management.tests.fixtures.load_fixtures import load_default_responses

from user_management.models.user_model import User
from Quizmos.selenium_tests.selenium_test_base import BaseSeleniumTest


class TestStudentPollResponses(TestCase, BaseSeleniumTest):
    """Tests that students can see and access polls they've responded to and their responses on their dashboard."""

    def setUp(self):
        super().setUp()

        # Set up all relevant fixtures
        create_default_test_user()
        create_default_test_polls()
        load_default_questions()
        load_default_responses()

        self.student = User.objects.get(username="janedoe")

        # Log in as student
        log_in(self.driver, self.live_server_url, self.student.username, "Password123")

        # Go to student dashboard
        student_dashboard_url = reverse("user_management:student_polls_page")
        self.driver.get(f"{self.live_server_url}{student_dashboard_url}")
        wait(self.driver)

    def tearDown(self):
        super().tearDown()


    def test_student_can_see_responded_polls(self):
        """Ensure the student can see the polls they've responded to and view each response in slideshow."""

        # Look for the "Your Polls" section header
        header = wait_for_element(self.driver, By.XPATH, "//h1[contains(text(), 'Your Polls')]")
        self.assertIsNotNone(header, "Could not find 'Your Polls' header.")

        view_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'View Responses')]")
        self.assertGreater(len(view_buttons), 0, "No 'View Responses' buttons found — expected at least one.")

        view_buttons[0].click()
        wait(self.driver)
        time.sleep(1)

        # On response slideshow
        slideshow_title = wait_for_element(self.driver, By.XPATH, "//h5[contains(text(), 'Question:')]")
        self.assertIsNotNone(slideshow_title, "Did not navigate to the response slideshow view.")

        # Scroll "Next" button into view before clicking
        next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        ActionChains(self.driver).move_to_element(next_button).perform()
        time.sleep(1)

        next_button.click()
        time.sleep(1)

        # Ensure it shows the next question
        next_question_title = wait_for_element(self.driver, By.XPATH, "//h5[contains(text(), 'Question:')]")
        self.assertIsNotNone(next_question_title, "Did not navigate to the next question.")


    def test_student_can_see_their_answer(self):
        """Ensure the student can see their answer on the screen."""

        header = wait_for_element(self.driver, By.XPATH, "//h1[contains(text(), 'Your Polls')]")
        self.assertIsNotNone(header, "Could not find 'Your Polls' header.")

        view_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'View Responses')]")
        self.assertGreater(len(view_buttons), 0, "No 'View Responses' buttons found — expected at least one.")

        view_buttons[0].click()
        wait(self.driver)
        time.sleep(1)

        # On response slideshow
        slideshow_title = wait_for_element(self.driver, By.XPATH, "//h5[contains(text(), 'Question:')]")
        self.assertIsNotNone(slideshow_title, "Did not navigate to the response slideshow view.")

        your_answer_element = wait_for_element(self.driver, By.ID, "your-answer-title")
        expected_title = "Your Answer:"
        self.assertEqual(expected_title, your_answer_element.text)








