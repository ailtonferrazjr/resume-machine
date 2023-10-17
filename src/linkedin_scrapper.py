from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os, dotenv

dotenv.load_dotenv()

class LinkedinBot:
    def __init__(self, credentials: dict):
        self.credentials = credentials
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
        time.sleep(1)
        self.webdriver.get(url=self.login_url)

        # Check if we already have the login cookies in this session
        if "linkedin.com/feed/" in self.webdriver.current_url:
            print("Login Succesfull!")
            time.sleep(2)
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

    def expand_my_profile(self):
        self.webdriver.get("https://www.linkedin.com/in/")
        time.sleep(5)
        all_see_more_buttons = self.webdriver.find_elements(
            By.CLASS_NAME, value="inline-show-more-text"
        )
        print(len(all_see_more_buttons))
        for button in all_see_more_buttons:
            time.sleep(0.5)
            # button.click()
            self.webdriver.execute_script("arguments[0].click();", button)

    # def scrape_my_profile(self):
    #     self.expand_my_profile()


if __name__ == "__main__":
    credentials = {"username": os.environ.get("EMAIL_LINKEDIN"), "password": os.environ.get("PASS_LINKEDIN")}
    linkedin_bot = LinkedinBot(credentials=credentials)
    login_sucessful = linkedin_bot.login_linkedin()
    if login_sucessful == True:
        linkedin_bot.expand_my_profile()
