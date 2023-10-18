from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gpt_api import CHATGPT

import time
import os, dotenv

dotenv.load_dotenv()


class LinkedinBot:
    def __init__(self, credentials: dict):
        self.credentials = credentials
        print("1) Initializing Bot!")
        self.login_url = "https://www.linkedin.com/login"
        self.success_login = self.initate_bot()

    def initate_bot(self) -> bool:
        """Function to initiate the bot, where it will return True or False depending on the success"""
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument(
            "--user-data-dir=/Users/justinferraz/Library/Application Support/Google/Chrome/Default"
        )
        self.webdriver = webdriver.Chrome(options=self.chrome_options)

    def login_linkedin(self):
        """Function to run the login process into linkedin"""

        # Access the website
        self.webdriver.get(url=self.login_url)
        time.sleep(2)

        # Check if we already have the login cookies in this session
        if "linkedin.com/feed/" in self.webdriver.current_url:
            print("2) Login Succesfull!")
            time.sleep(0.5)
            return True

        time.sleep(1)

        # Locate the email and password fields
        email_field = self.webdriver.find_element(By.ID, value="username")
        password_field = self.webdriver.find_element(By.ID, value="password")
        submit_button = self.webdriver.find_element(
            By.CLASS_NAME, value="btn__primary--large"
        )

        # Fill the email and password fields
        time.sleep(2)
        email_field.send_keys(self.credentials["username"])
        time.sleep(2)
        password_field.send_keys(self.credentials["password"])
        time.sleep(2)
        submit_button.click()
        time.sleep(2)

        # Check if the login is sucessful, otherwise recursively call the function again
        if "linkedin.com/feed/" in self.webdriver.current_url:
            print("Login Succesfull!")
            return True
        else:
            input("Press a button when you did the captcha to try again!")
            self.login_linkedin()

    def terminate_bot(self):
        self.webdriver.quit()

    def scrape_my_profile(self):
        profile_page = self.webdriver.get("https://www.linkedin.com/in/")
        print("3) Going to profile page")
        time.sleep(5)

        # Scroll down multiple times to make sure all elements get loaded
        for _ in range(5):  # You can adjust the range as needed
            self.webdriver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)  # Wait for elements to load after each scroll

        experience_section = self.webdriver.find_element(
            By.XPATH, value="//main/section[7]"
        )
        outer_html = experience_section.get_attribute("outerHTML")
        print(f"Experience section scrapped with {len(outer_html)} total characters")
        return outer_html


if __name__ == "__main__":
    credentials = {
        "username": os.environ.get("EMAIL_LINKEDIN"),
        "password": os.environ.get("PASS_LINKEDIN"),
    }
    linkedin_bot = LinkedinBot(credentials=credentials)
    login_sucessful = linkedin_bot.login_linkedin()
    if login_sucessful == True:
        my_profile = linkedin_bot.scrape_my_profile()
        time.sleep(1)
        print("4) Calling ChatGPT API")
        response = CHATGPT.send_html(html=my_profile)
        print(response)
        # linkedin_bot.terminate_bot()
