import time
from django.test import TestCase
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from django.shortcuts import reverse
import ast  # To safely convert string to list
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

from Quizmos.selenium_tests import log_in, wait, wait_for_clickable, wait_for_element, safe_click  # From __init__.py
from poll_management.tests.fixtures.create_test_polls import create_default_test_polls
from user_management.tests.fixtures.create_test_users import create_default_test_user
from question_management.tests.fixtures.load_fixtures import load_default_questions
from user_management.models.user_model import User
from poll_management.models.poll_model import Poll
from Quizmos.selenium_tests.selenium_test_base import BaseSeleniumTest


class TestFunctionalAddQuestionManagement(TestCase, BaseSeleniumTest):
    """This class tests all question functionality to check that users can create questions of varying types."""
    def setUp(self):
        super().setUp()

        # From fixtures folders in relative apps
        create_default_test_user()
        create_default_test_polls()
        self.lecturer = User.objects.get(role='Lecturer')
        self.poll = Poll.objects.get(pk=1)

        log_in(self.driver, self.live_server_url, self.lecturer.username, 'Password123')
        self.driver.get(f"{self.live_server_url}{reverse('user_management:dashboard')}")


    def tearDown(self):
        super().tearDown()

    # Helper methods below:

    def add_two_options_for_choice_questions(self, add_option_button):
        """Helper to add options for multiple and single choice questions."""
        # First Option
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_option_button)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", add_option_button)
        alert = Alert(self.driver)
        alert.send_keys("Paris")
        alert.accept()
        wait(self.driver)

        # Second Option
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_option_button)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", add_option_button)
        alert.send_keys("London")
        alert.accept()
        wait(self.driver)

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

    # End of helper methods

    def test_add_text_fill_question(self):
        self.navigate_to_edit_poll()

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

    def test_user_can_add_multiple_choice_question(self):
        self.navigate_to_edit_poll()

        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value("multiple_choice")
        wait(self.driver)

        question_input = self.driver.find_element(By.NAME, "multiple_choice_question")
        question_input.send_keys("What is the capital of France?")

        add_option_button = wait_for_clickable(self.driver,
                                               self.driver.find_element(By.ID, "multiple-choice-add-option-btn"))
        self.add_two_options_for_choice_questions(add_option_button)

        option_inputs = self.driver.find_elements(By.CSS_SELECTOR, "#multiple-choice-options-container input")
        unique_options = list(set([opt.get_attribute("value").strip() for opt in option_inputs]))
        self.assertEqual(len(unique_options), 2)

        paris_checkbox = self.driver.find_element(By.XPATH,
                                                  "//label[text()='Paris']/preceding-sibling::input[@type='checkbox']")
        paris_checkbox.click()
        wait(self.driver)
        time.sleep(1)

        save_btn = self.driver.find_element(By.ID, "id_save_question_button")
        safe_click(self.driver, save_btn)
        time.sleep(1)

        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        multiple_choice_answers = question.multiple_choice_answers
        self.assertIn('Paris', multiple_choice_answers)

    def test_user_can_add_single_choice_question(self):
        self.navigate_to_edit_poll()

        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value("single_choice")
        wait(self.driver)

        question_input = self.driver.find_element(By.NAME, "single_choice_question")
        question_input.send_keys("What is the capital of France?")

        add_option_button = wait_for_clickable(self.driver,
                                               self.driver.find_element(By.ID, "single-choice-add-option-btn"))
        self.add_two_options_for_choice_questions(add_option_button)

        option_inputs = self.driver.find_elements(By.CSS_SELECTOR,
                                                  "#single-choice-options-container input")

        unique_options = list(set([opt.get_attribute("value").strip() for opt in option_inputs]))

        self.assertEqual(len(unique_options), 2)
        self.assertIn("Paris", unique_options)

        label = self.driver.find_element(By.XPATH, "//label[text()='Paris']")
        radio_id = label.get_attribute("for")
        paris_radio = self.driver.find_element(By.ID, radio_id)
        paris_radio.click()
        wait(self.driver)

        save_btn = self.driver.find_element(By.ID, "id_save_question_button")
        safe_click(self.driver, save_btn)
        time.sleep(1)

        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        single_choice_answers = question.single_choice_answers
        self.assertIn("Paris", single_choice_answers)

    def test_user_can_add_dropdown_question(self):
        self.navigate_to_edit_poll()

        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value("dropdown_fill")
        wait(self.driver)

        dropdown_input = wait_for_element(self.driver, By.ID, "dropdown-fill-input")
        dropdown_input.send_keys("The capital of France is Paris")

        text_preview = wait_for_element(self.driver, By.ID, "text-preview")
        word_to_click = text_preview.find_element(By.XPATH, ".//span[contains(text(),'Paris')]")

        self.driver.execute_script("arguments[0].scrollIntoView(true);", word_to_click)
        time.sleep(0.5)  # Add delay to ensure scroll happens

        word_to_click = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//span[contains(text(),'Paris')]"))
        )
        word_to_click.click()

        wait(self.driver)
        correct_answer_field = wait_for_element(self.driver, By.ID, "dropdown-correct-answer")
        self.assertEqual(correct_answer_field.get_attribute("value"), "Paris")

        self.assertEqual(dropdown_input.get_attribute("value"), "The capital of France is _____")

        additional_options = self.driver.find_elements(By.NAME, "additional_options")
        incorrect_answers = ["London", "Berlin", "Madrid"]
        for input_box, incorrect_answer in zip(additional_options, incorrect_answers):
            input_box.send_keys(incorrect_answer)
            self.assertEqual(input_box.get_attribute("value"), incorrect_answer)

        save_btn = self.driver.find_element(By.ID, "id_save_question_button")
        safe_click(self.driver, save_btn)
        time.sleep(1)

        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        self.assertEqual(question.dropdown_fill_question, "The capital of France is _____")
        self.assertEqual(question.dropdown_answer, "Paris")

    def test_user_can_add_match_question(self):
        self.navigate_to_edit_poll()

        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value("match_question")
        wait(self.driver)

        match_question_input = wait_for_element(self.driver, By.NAME, "match_question")
        match_question_input.send_keys("Match the following items.")

        add_option_btn = wait_for_element(self.driver, By.ID, "match-add-option-btn")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_option_btn)  # Scroll the button into view
        wait_for_clickable(self.driver, add_option_btn).click()  # Wait for clickability and click

        match_option = wait_for_element(self.driver, By.NAME, "match_question_options[]")
        match_answer = wait_for_element(self.driver, By.NAME, "match_question_answers[]")

        match_option.clear()
        match_option.send_keys("Apple")
        match_answer.clear()
        match_answer.send_keys("Fruit")

        self.assertEqual(match_option.get_attribute("value"), "Apple")
        self.assertEqual(match_answer.get_attribute("value"), "Fruit")

        self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                   add_option_btn)  # Scroll the button into view again
        wait_for_clickable(self.driver, add_option_btn).click()  # Click to add a second pair
        wait(self.driver)

        # Get all the option and answer fields now (find_elements will return a list)
        match_option_fields = self.driver.find_elements(By.NAME, "match_question_options[]")
        match_answer_fields = self.driver.find_elements(By.NAME, "match_question_answers[]")

        match_option = match_option_fields[1]  # Second option
        match_answer = match_answer_fields[1]  # Second answer

        match_option.clear()
        match_option.send_keys("Carrot")
        match_answer.clear()
        match_answer.send_keys("Vegetable")

        self.assertEqual(match_option.get_attribute("value"), "Carrot")
        self.assertEqual(match_answer.get_attribute("value"), "Vegetable")

        save_btn = self.driver.find_element(By.ID, "id_save_question_button")
        safe_click(self.driver, save_btn)
        time.sleep(1)

        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        self.assertEqual(question.match_question, "Match the following items.")
        match_options = question.match_options
        match_answers = question.match_answers
        self.assertIn("Apple", match_options)
        self.assertIn("Fruit", match_answers)
        self.assertIn("Carrot", match_options)
        self.assertIn("Vegetable", match_answers)


class TestFunctionalEditQuestionManagement(TestCase, BaseSeleniumTest):
    """This class tests all question functionality to check that users can create questions of varying types."""
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

        # Go to edit poll page
        edit_button = wait_for_element(self.driver, By.ID, "id_poll_edit_button")
        safe_click(self.driver, edit_button)
        wait(self.driver)
        time.sleep(1)

    def tearDown(self):
        super().tearDown()

    def test_edit_question(self):
        """Test editing an existing question."""
        question = self.poll.questions.all()[2]  # Select the third question (text fill)

        edit_button = wait_for_element(self.driver, By.XPATH,
                                       f"//div[@data-id='{question.id}']//a[contains(@class, 'btn-warning')]")
        safe_click(self.driver, edit_button)
        wait(self.driver)

        try:
            if question.question_type == "text_fill":
                question_input = wait_for_element(self.driver, By.NAME, "text_fill_answer")
                self.driver.execute_script("arguments[0].scrollIntoView();", question_input)
                question_input.clear()
                question_input.send_keys("Updated Answer")

            save_button = wait_for_element(self.driver, By.XPATH, "//button[contains(text(), 'Save Changes')]")
            safe_click(self.driver, save_button)
            wait(self.driver)

            # Revisit the edit page to verify the change (Navigate back to the edit page)
            self.driver.get(self.driver.current_url)  # This will refresh the page or re-navigate
            edit_button = wait_for_element(self.driver, By.XPATH,
                                           f"//div[@data-id='{question.id}']//a[contains(@class, 'btn-warning')]")
            safe_click(self.driver, edit_button)
            wait(self.driver)

            question_input = wait_for_element(self.driver, By.NAME, "text_fill_answer")
            self.assertEqual(question_input.get_attribute("value"), "Updated Answer")

        except TimeoutException:
            self.fail("Edit question input field not found")
