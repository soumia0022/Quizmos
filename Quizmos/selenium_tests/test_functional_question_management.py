import time
from django.test import TestCase
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from django.shortcuts import reverse
import ast  # To safely convert string to list

from Quizmos.selenium_tests import log_in, wait, wait_for_clickable, wait_for_element  # From __init__.py
from poll_management.tests.fixtures.create_test_polls import create_default_test_polls
from user_management.tests.fixtures.create_test_users import create_default_test_user
from user_management.models.user_model import User
from poll_management.models.poll_model import Poll
from Quizmos.selenium_tests.selenium_test_base import BaseSeleniumTest

# Need to test constraints i.e. what happens if a user does not select a multiple choice option
# Discuss with team about testing add audio and add video, I think this will be better to test on the lecturer side
# where the audio/video has actually been embedded, rather than just checking the upload which has already been covered
# by other non-selenium testing.
# Can test deletion (deletion of choice and match options & reset dropdown) but this has been covered by non-selenium tests

class TestFunctionalAddQuestionManagement(TestCase, BaseSeleniumTest):
    """This class tests all question functionality to check that users can create questions of varying types."""
    def setUp(self):
        super().setUp()

        # From fixtures folders in relative apps
        create_default_test_user()
        create_default_test_polls()
        self.lecturer = User.objects.get(role='Lecturer')
        self.poll = Poll.objects.get(pk=1)

        # Navigate to add question page once logging in
        log_in(self.driver, self.live_server_url, self.lecturer.username, 'Password123')
        self.driver.get(f"{self.live_server_url}{reverse('user_management:dashboard')}")
        edit_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_poll_edit_button"))
        edit_button.click()
        edit_questions_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_edit_questions_button"))
        edit_questions_button.click()
        add_question_button = wait_for_element(self.driver, By.ID, "add-question-btn")  # ID already given
        add_question_button.click()
        wait(self.driver)

    def tearDown(self):
        super().tearDown()

    def test_user_can_add_multiple_choice_question(self):
        # Test if Multiple Choice Option can be selected
        self.select_question("multiple_choice", "multiple-choice-fields")

        # Test the creation of a Multiple Choice Question
        question_input = self.driver.find_element(By.NAME, "multiple_choice_question")
        question_input.send_keys("What is the capital of France?")
        add_option_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "multiple-choice-add-option-btn"))
        self.add_two_options_for_choice_questions(add_option_button)
        option_inputs = self.driver.find_elements(By.CSS_SELECTOR, "#multiple-choice-options-container input")  # Verify options appear in the form after closing the popup
        unique_options = list(set([opt.get_attribute("value").strip() for opt in option_inputs]))
        self.assertEqual(len(unique_options), 2)  # Should be only "Paris" and "London"
        paris_checkbox = self.driver.find_element(By.XPATH, "//label[text()='Paris']/preceding-sibling::input[@type='checkbox']")
        paris_checkbox.click()  # Check the correct option
        wait(self.driver)
        time.sleep(1)

        # Test the saving of a Multiple Choice Question (verify in database)
        self.save_question()
        time.sleep(1)
        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        multiple_choice_answers = question.multiple_choice_answers  # List of selected (correct) answers
        self.assertIn('Paris', multiple_choice_answers)

    def test_user_can_add_single_choice_question(self):
        # Test if Single Choice Option can be selected
        self.select_question("single_choice", "single-choice-fields")

        # Test the creation of a Single Choice Question
        question_input = self.driver.find_element(By.NAME, "single_choice_question")
        question_input.send_keys("What is the capital of France?")
        add_option_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "single-choice-add-option-btn"))
        self.add_two_options_for_choice_questions(add_option_button)
        option_inputs = self.driver.find_elements(By.CSS_SELECTOR, "#single-choice-options-container input")  # Verify options appear in the form after closing the popup
        unique_options = list(set([opt.get_attribute("value").strip() for opt in option_inputs]))
        self.assertEqual(len(unique_options), 2)  # Should be only "Paris" and "London"
        paris_checkbox = self.driver.find_element(By.XPATH, "//label[text()='Paris']/preceding-sibling::input[@type='checkbox']")
        paris_checkbox.click()  # Check the correct option
        wait(self.driver)
        time.sleep(1)

        # Test the saving of a Single Choice Question (verify in database)
        self.save_question()
        time.sleep(1)
        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        single_choice_answers = question.single_choice_answers  # List of selected (correct) answers
        self.assertIn('Paris', single_choice_answers)

    def test_user_can_add_text_question(self):
        # Test if Text can be selected
        self.select_question("text_fill", "text-fill-fields")

        # Test the creation of a Text Fill question
        text_question_input = wait_for_element(self.driver, By.ID, "id_text_question")
        text_question_input.send_keys("What is the capital of France?")
        text_answer_input = wait_for_element(self.driver, By.ID, "id_text_answer")
        text_answer_input.send_keys("Paris")
        wait(self.driver)

        # Test the saving of a Text Fill question (verify in database)
        self.save_question()
        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        text_fill_answer = question.text_fill_answer
        self.assertIn('Paris', text_fill_answer)

    def test_user_can_add_dropdown_question(self):
        # Test if Text can be selected
        self.select_question("dropdown_fill", "dropdown-fill-fields")

        # Test the creation of a Dropdown Fill question
        dropdown_input = wait_for_element(self.driver, By.ID, "dropdown-fill-input")
        dropdown_input.send_keys("The capital of France is Paris")
        text_preview = wait_for_element(self.driver, By.ID, "text-preview")
        self.assertIn("The capital of France is Paris", text_preview.text)  # Verify preview updates
        word_to_click = text_preview.find_element(By.XPATH, ".//span[contains(text(),'Paris')]")
        word_to_click.click()
        correct_answer_field = wait_for_element(self.driver, By.ID, "dropdown-correct-answer")
        self.assertEqual(correct_answer_field.get_attribute("value"), "Paris")
        self.assertEqual(dropdown_input.get_attribute("value"), "The capital of France is _____")  # Verify blank space
        additional_options = self.driver.find_elements(By.NAME, "additional_options")
        incorrect_answers = ["London", "Berlin", "Madrid"]
        for input_box, incorrect_answer in zip(additional_options, incorrect_answers):
            input_box.send_keys(incorrect_answer)
            self.assertEqual(input_box.get_attribute("value"), incorrect_answer)

        # Test the saving of a Dropdown Question (verify in database)
        self.save_question()
        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        dropdown_question_text = question.dropdown_fill_question
        correct_answer = question.dropdown_answer
        self.assertEqual(dropdown_question_text, "The capital of France is _____")
        self.assertEqual(correct_answer, "Paris")

    def test_user_can_add_word_cloud_question(self):
        # Test if Word Cloud can be selected
        self.select_question("wordcloud", "word-cloud-fields")

        # Test the creation of a Word Cloud question
        word_cloud_question_input = wait_for_element(self.driver, By.ID, "id_word_cloud_question")
        word_cloud_question_input.send_keys("Name some cities in France")
        wait(self.driver)

        # Test the saving of a Word Cloud question (verify in database)
        self.save_question()
        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        wordcloud_question = question.wordcloud_question
        self.assertIn('Name some cities in France', wordcloud_question)

    def test_user_can_add_match_question(self):
        # Test if Match Question can be selected
        self.select_question("match_question", "match-fields")

        # Test the creation of a Match question
        match_question_input = wait_for_element(self.driver, By.NAME, "match_question")
        match_question_input.send_keys("Match the following items.")
        add_option_btn = wait_for_element(self.driver, By.ID, "match-add-option-btn")
        wait_for_clickable(self.driver, add_option_btn).click()
        match_option = wait_for_element(self.driver, By.NAME, "match_question_options[]")
        match_answer = wait_for_element(self.driver, By.NAME, "match_question_answers[]")
        match_option.send_keys("Apple")
        match_answer.send_keys("Fruit")
        self.assertEqual(match_option.get_attribute("value"), "Apple")
        self.assertEqual(match_answer.get_attribute("value"), "Fruit")

        # Test the saving of a Match question (verify in database)
        self.save_question()
        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        match_question_text = question.match_question
        self.assertEqual(match_question_text, "Match the following items.")

    # def test_user_can_add_code_question(self):
    #     # Test if Code Question can be selected
    #     self.select_question("code_question", "code-question-fields")
    #
    #     # Test the creation of a Code question
    #     code_question_input = wait_for_element(self.driver, By.ID, "id_code_question")
    #     code_question_input.send_keys("Allow the user to input the capital of France and print the answer with an ! at the end")
    #     code_language_dropdown = Select(self.driver.find_element("name", "code_language"))
    #     code_language_dropdown.select_by_value("python")
    #     code_answer_input = wait_for_element(self.driver, By.ID, "id_code_answer")
    #     code_answer_input.send_keys('[{"input": "Paris", "output": "Paris!"}]')
    #     wait(self.driver)
    #
    #     # Test the saving of a Code question (verify in database)
    #     self.save_question()
    #     poll = Poll.objects.get(id=self.poll.id)
    #     question = poll.questions.last()
    #     code_test_cases = question.code_test_cases
    #     expected_test_case = "[{'input': 'Paris', 'output': 'Paris!'}]"
    #     expected_test_case = ast.literal_eval(expected_test_case)  # Convert to a list
    #     self.assertIn(expected_test_case[0], code_test_cases)


    # Helper methods below:

    def select_question(self, question_type, question_fields):
        """Checks that the question type being tested can be selected from the question dropdown."""
        dropdown = Select(wait_for_element(self.driver, By.ID, "question-type-dropdown"))
        dropdown.select_by_value(question_type)
        selected_option = dropdown.first_selected_option
        self.assertEqual(selected_option.get_dom_attribute("value"), question_type)
        question_fields = wait_for_element(self.driver, By.ID, question_fields)
        self.assertTrue(question_fields.is_displayed())

    def add_two_options_for_choice_questions(self, add_option_button):
        add_option_button.click()
        alert = Alert(self.driver)  # Wait for alert popup and enter first option
        alert.send_keys("Paris")
        alert.accept()
        wait(self.driver)
        add_option_button.click()  # Click "Add Option" again for second choice
        alert.send_keys("London")
        alert.accept()
        wait(self.driver)

    def save_question(self):
        save_button = wait_for_element(self.driver, By.ID, "id_save_question_button")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        try:
            wait_for_clickable(self.driver, save_button).click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", save_button)  # Click via JS
        time.sleep(2)

    # End of helper methods

class TestFunctionalEditQuestionManagement(TestCase, BaseSeleniumTest):
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
        wait(self.driver)
        edit_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_poll_edit_button"))
        edit_button.click()
        wait(self.driver)

    def tearDown(self):
        super().tearDown()

    def test_user_can_attempt_to_edit_questions(self):
        edit_questions_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_edit_questions_button"))
        edit_questions_button.click()
        wait(self.driver)

        add_question_title_element = wait_for_element(self.driver, By.ID, "id_add_question_title")  # From add_question.html
        expected_title = "Sample Poll"
        self.assertEqual(expected_title, add_question_title_element.text)
        add_question_button = wait_for_element(self.driver, By.ID, "add-question-btn")  # ID already given
        self.assertTrue(add_question_button.is_displayed(), "'Add Question' button is not visible!")