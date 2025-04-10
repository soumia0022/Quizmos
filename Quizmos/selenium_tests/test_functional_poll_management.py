from django.test import TestCase
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from django.shortcuts import reverse
import time

from selenium.webdriver.support.select import Select

from Quizmos.selenium_tests import log_in, wait, wait_for_clickable, wait_for_element, safe_click  # From __init__.py
from poll_management.tests.fixtures.create_test_polls import create_default_test_polls
from user_management.tests.fixtures.create_test_users import create_default_test_user
from question_management.tests.fixtures.load_fixtures import load_default_questions
from user_management.models.user_model import User
from poll_management.models.poll_model import Poll
from Quizmos.selenium_tests.selenium_test_base import BaseSeleniumTest


class TestFunctionalPollManagement(TestCase, BaseSeleniumTest):
    """This class tests all poll functionality (excluding question specific functionality)."""
    def setUp(self):
        super().setUp()

        # From fixtures folders in relative apps
        create_default_test_user()
        create_default_test_polls()
        load_default_questions()
        self.lecturer = User.objects.get(role='Lecturer')
        self.poll = Poll.objects.get(pk=1)

        log_in(self.driver, self.live_server_url, self.lecturer.username, 'Password123')
        self.driver.get(f"{self.live_server_url}{reverse('user_management:dashboard')}")
        wait(self.driver)

    def tearDown(self):
        super().tearDown()

    def test_user_can_edit_poll(self):
        edit_button = wait_for_element(self.driver, By.ID, "id_poll_edit_button")
        safe_click(self.driver, edit_button)
        wait(self.driver)
        time.sleep(1)

        title_input = wait_for_element(self.driver, By.ID, "id_poll_title")
        self.assertEqual(title_input.get_attribute("value"), "Sample Poll")

        title_input.clear()
        title_input.send_keys("Edited Title")

        save_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        safe_click(self.driver, save_button)
        wait(self.driver)
        time.sleep(1)

        updated_title_input = wait_for_element(self.driver, By.ID, "id_poll_title")
        self.assertEqual(updated_title_input.get_attribute("value"), "Edited Title")

    def test_user_can_delete_poll(self):
        delete_button = self.driver.find_element(By.ID, "id_poll_delete_button")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", delete_button)
        safe_click(self.driver, delete_button)

        wait_for_element(self.driver, By.ID, "custom-popup")

        confirm_button = self.driver.find_element(By.ID, "confirm-delete")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                   confirm_button)
        wait_for_clickable(self.driver, confirm_button).click()

        wait(self.driver)
        time.sleep(1)

        self.assertFalse(Poll.objects.filter(pk=self.poll.id).exists(), "Poll was not deleted!")

    def test_lecturer_can_start_a_poll_and_present_all_questions(self):
        start_button = wait_for_element(self.driver, By.ID, "id_poll_start_button")

        # Check it's enabled and click
        self.assertFalse("disabled" in start_button.get_attribute("class"))
        safe_click(self.driver, start_button)
        wait(self.driver)

        title_element = wait_for_element(self.driver, By.ID, "id_start_poll_title")
        self.assertEqual(title_element.text.strip(), "Sample Poll")

        start_poll_button = wait_for_element(self.driver, By.ID, "start-poll-btn")
        safe_click(self.driver, start_poll_button)
        wait(self.driver)

        # Define expected questions in order (taken from fixtures)
        expected_questions = [
            "Which of these are programming languages?",
            "What is the capital of France?",
            "Name a primary color.",
            "A banana is usually the colour",
            "Match the country to its capital.",
            "What word comes to mind when you think of 'ocean'?",
            "Write a function that returns the square of a number.",
        ]

        # Loop through all questions
        for index, expected_text in enumerate(expected_questions):
            question_container = wait_for_element(self.driver, By.ID, "question-container")
            self.assertIn(expected_text, question_container.text)

            # Only click "Next" if not on the last question
            if index < len(expected_questions) - 1:
                next_btn = wait_for_element(self.driver, By.ID, "next-btn")
                self.assertFalse(next_btn.get_attribute("disabled"))
                safe_click(self.driver, next_btn)
                wait(self.driver)



