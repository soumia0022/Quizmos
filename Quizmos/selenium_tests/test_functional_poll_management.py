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

    def navigate_to_edit_poll(self):
        """Helper method to navigate to the edit poll page."""
        # Go to edit poll page
        edit_button = wait_for_element(self.driver, By.ID, "id_poll_edit_button")
        safe_click(self.driver, edit_button)
        wait(self.driver)
        time.sleep(1)

        # Click Add Question to reveal form
        add_question_btn = wait_for_element(self.driver, By.ID, "add-question-btn")
        safe_click(self.driver, add_question_btn)
        wait(self.driver)
        time.sleep(1)

    def select_question(self, question_type_value, container_id):
        # Open the question form if it's not visible yet
        try:
            add_btn = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "add-question-btn"))
            add_btn.click()
        except Exception as e:
            pass  # Already open or handled

        # Wait for the dropdown to appear
        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value(question_type_value)

        # Wait for the specific fields container to load
        wait_for_element(self.driver, By.ID, container_id)

    def save_question(self):
        save_button = wait_for_element(self.driver, By.ID, "id_save_question_button")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        try:
            wait_for_clickable(self.driver, save_button).click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", save_button)  # Click via JS
        time.sleep(2)

        # End of helper methods

    def test_add_text_fill_question(self):
        self.navigate_to_edit_poll()

        # Select "Text Answer" from dropdown
        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value("text_fill")

        wait(self.driver)
        text_q = self.driver.find_element(By.ID, "id_text_question")
        text_a = self.driver.find_element(By.ID, "id_text_answer")
        text_q.send_keys("What is your favorite color?")
        text_a.send_keys("Blue")

        save_btn = self.driver.find_element(By.ID, "id_save_question_button")
        safe_click(self.driver, save_btn)
        wait(self.driver)


    def test_add_word_cloud_question(self):
        self.navigate_to_edit_poll()

        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value("wordcloud")
        wait(self.driver)

        wordcloud_input = self.driver.find_element(By.ID, "id_word_cloud_question")
        wordcloud_input.send_keys("Describe your mood in one word")

        save_btn = self.driver.find_element(By.ID, "id_save_question_button")
        safe_click(self.driver, save_btn)
        wait(self.driver)

    def test_add_code_question(self):
        self.navigate_to_edit_poll()

        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value("code_question")
        wait(self.driver)

        question_text = self.driver.find_element(By.ID, "id_code_question")
        question_text.send_keys("Write a function that returns the square of a number")

        language_select = Select(self.driver.find_element(By.ID, "language-selector"))
        language_select.select_by_value("python")

        code_editor = self.driver.find_element(By.CLASS_NAME, "CodeMirror")
        self.driver.execute_script("arguments[0].CodeMirror.setValue(arguments[1])", code_editor,
                                   "def square(n): return n * n")

        save_btn = self.driver.find_element(By.ID, "id_save_question_button")
        safe_click(self.driver, save_btn)
        wait(self.driver)



    # def test_user_can_see_poll_start_page_and_start_poll(self):
    #     start_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "id_poll_start_button"))
    #     start_button.click()
    #     wait(self.driver)
    #
    #     start_poll_title_element = wait_for_element(self.driver, By.ID, "id_start_poll_title")  # From display_code.html
    #     expected_title = "Sample Poll"
    #     self.assertEqual(expected_title, start_poll_title_element.text)
    #
    #     start_poll_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "start-poll-btn"))  # Already given ID by another group member
    #     start_poll_button.click()
    #     wait(self.driver)
    #
    #     prev_button = wait_for_element(self.driver, By.ID, "prev-btn")  # ID already given
    #     next_button = wait_for_element(self.driver, By.ID, "next-btn")  # ID already given
    #     self.assertTrue(prev_button.is_displayed(), "'Prev' button is not visible!")
    #     self.assertTrue(next_button.is_displayed(), "'Next' button is not visible!")
