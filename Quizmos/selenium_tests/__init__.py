import logging
from django.shortcuts import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver  # Allows browser automation


# Only critical errors logged
logging.getLogger("selenium").setLevel(logging.CRITICAL)
logging.getLogger("django.request").setLevel(logging.CRITICAL)


def log_in(driver: WebDriver, live_server_url: str, username: str, password: str):
    """Automates the login process for a user in Selenium."""
    driver.get(f"{live_server_url}{reverse('user_management:log_in')}")  # Navigate to login page
    wait(driver)  # Wait for the page to fully load before interacting

    # Find input fields and log in button
    username_input = driver.find_element(By.ID, "id_username")  # Generated automatically from form field username
    password_input = driver.find_element(By.ID, "id_password")  # Generated automatically from form field password
    login_button = driver.find_element(By.ID, "id_log_in_button")  # In log_in.html

    # Send keys is used to type in the username and password
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()  # Called on the login button to submit the form

    wait(driver)

def logout(driver: WebDriver, live_server_url: str):
    driver.get(f"{live_server_url}{reverse('user_management:log_out')}")

def wait(driver_client):
    """Ensures page is fully loaded before continuing."""

    WebDriverWait(driver_client, 60).until(

        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

def wait_for_element(driver_client, by, value, timeout=100):
    """Waits for element to be fully present in the DOM."""
    return WebDriverWait(driver_client, timeout).until(
        EC.presence_of_element_located((by, value))  # Element found
    )

def wait_for_clickable(driver_client, elem: WebElement, timeout=100):
    """Waits for an element to become clickable."""
    return WebDriverWait(driver_client, timeout).until(
        EC.element_to_be_clickable(elem)
    )