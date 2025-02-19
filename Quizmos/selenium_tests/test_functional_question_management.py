import time
from django.test import TestCase
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from django.shortcuts import reverse

from Quizmos.selenium_tests import log_in, wait, wait_for_clickable, wait_for_element  # From __init__.py
from poll_management.tests.fixtures.create_test_polls import create_default_test_polls
from user_management.tests.fixtures.create_test_users import create_default_test_user
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

    def test_user_can_add_multiple_choice_question(self):
        # Navigate to add question page
        edit_questions_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_edit_questions_button"))
        edit_questions_button.click()
        wait(self.driver)
        add_question_button = wait_for_element(self.driver, By.ID, "add-question-btn")  # ID already given
        add_question_button.click()
        wait(self.driver)

        # Test if Multiple Choice Option can be selected
        dropdown_question_type_element = wait_for_element(self.driver, By.ID, "question-type-dropdown")
        dropdown = Select(dropdown_question_type_element)
        dropdown.select_by_value("multiple_choice")
        # time.sleep(2)
        selected_option = dropdown.first_selected_option
        self.assertEqual(selected_option.get_dom_attribute("value"), "multiple_choice")
        multiple_choice_fields = wait_for_element(self.driver, By.ID, "multiple-choice-fields")
        self.assertTrue(multiple_choice_fields.is_displayed())

        # Test the creation of a Multiple Choice Question
        question_input = self.driver.find_element(By.NAME, "multiple_choice_question")
        question_input.send_keys("What is the capital of France?")
        add_option_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "multiple-choice-add-option-btn"))
        add_option_button.click()

        alert = Alert(self.driver)  # Wait for alert popup and enter first option
        alert.send_keys("Paris")
        alert.accept()
        wait(self.driver)
        add_option_button.click()  # Click "Add Option" again for second choice
        alert.send_keys("London")
        alert.accept()
        wait(self.driver)

        option_inputs = self.driver.find_elements(By.CSS_SELECTOR, "#multiple-choice-options-container input")  # Verify options appear in the form after closing the popup
        unique_options = list(set([opt.get_attribute("value").strip() for opt in option_inputs]))
        # print("Unique options:", unique_options)
        self.assertEqual(len(unique_options), 2)  # Should be only "Paris" and "London"
        paris_checkbox = self.driver.find_element(By.XPATH, "//label[text()='Paris']/preceding-sibling::input[@type='checkbox']")
        paris_checkbox.click()  # Check the correct option

        # Test the saving of a Multiple Choice Question (verify in database)
        save_button = self.driver.find_element(By.ID, "id_save_question_button")
        save_button.click()
        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        multiple_choice_answers = question.multiple_choice_answers  # List of selected (correct) answers
        self.assertIn('Paris', multiple_choice_answers)

    def test_user_can_add_single_choice_question(self):
        # Navigate to add question page
        edit_questions_button = wait_for_clickable(self.driver, wait_for_element(self.driver, By.ID, "id_edit_questions_button"))
        edit_questions_button.click()
        wait(self.driver)
        add_question_button = wait_for_element(self.driver, By.ID, "add-question-btn")  # ID already given
        add_question_button.click()
        wait(self.driver)

        # Test if Multiple Choice Option can be selected
        dropdown_question_type_element = wait_for_element(self.driver, By.ID, "question-type-dropdown")
        dropdown = Select(dropdown_question_type_element)
        dropdown.select_by_value("single_choice")
        # time.sleep(2)
        selected_option = dropdown.first_selected_option
        self.assertEqual(selected_option.get_dom_attribute("value"), "single_choice")
        single_choice_fields = wait_for_element(self.driver, By.ID, "single-choice-fields")
        self.assertTrue(single_choice_fields.is_displayed())

        # Test the creation of a Multiple Choice Question
        question_input = self.driver.find_element(By.NAME, "single_choice_question")
        question_input.send_keys("What is the capital of France?")
        add_option_button = wait_for_clickable(self.driver, self.driver.find_element(By.ID, "single-choice-add-option-btn"))
        add_option_button.click()

        alert = Alert(self.driver)  # Wait for alert popup and enter first option
        alert.send_keys("Paris")
        alert.accept()
        wait(self.driver)
        add_option_button.click()  # Click "Add Option" again for second choice
        alert.send_keys("London")
        alert.accept()
        wait(self.driver)

        option_inputs = self.driver.find_elements(By.CSS_SELECTOR, "#single-choice-options-container input")  # Verify options appear in the form after closing the popup
        unique_options = list(set([opt.get_attribute("value").strip() for opt in option_inputs]))
        # print("Unique options:", unique_options)
        self.assertEqual(len(unique_options), 2)  # Should be only "Paris" and "London"
        paris_checkbox = self.driver.find_element(By.XPATH, "//label[text()='Paris']/preceding-sibling::input[@type='checkbox']")
        paris_checkbox.click()  # Check the correct option

        # Test the saving of a Multiple Choice Question (verify in database)
        save_button = self.driver.find_element(By.ID, "id_save_question_button")
        save_button.click()
        poll = Poll.objects.get(id=self.poll.id)
        question = poll.questions.last()
        single_choice_answers = question.single_choice_answers  # List of selected (correct) answers
        self.assertIn('Paris', single_choice_answers)


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