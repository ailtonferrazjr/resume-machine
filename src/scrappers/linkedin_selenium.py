from selenium import webdriver
from selenium.webdriver.common.by import By
import os, dotenv
import time
from scrapper_log import ScrappingLogs
from linkedin_parser import LinkedinParser

dotenv.load_dotenv()
print("oi")

CREDENTIALS = {
    "username": os.environ.get("EMAIL_LINKEDIN"),
    "password": os.environ.get("PASSWORD_LINKEDIN"),
}

SHORT_DELAY = 2
LONG_DELAY = 5

PAGES_TO_SCRAPE = ["experience", "education", "skills"]


class LinkedinBot:
    """Class created to run all methods related to scrappying Linkedin"""

    def __init__(self, credentials: dict):
        self.credentials = credentials
        self.load_logs()
        self.load_constants()

    def load_constants(self):
        self.pages_to_scrape = PAGES_TO_SCRAPE

    def load_logs(self) -> None:
        self.logs = ScrappingLogs()
        self.logs_data = self.logs.data
        print("Logs loaded!")

    def setup_chrome_options(self) -> bool:
        """Function to set chrome options to the bot"""
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument(
            "--user-data-dir=/Users/justinferraz/Library/Application Support/Google/Chrome/Default"
        )

    def create_session(self):
        ## Initiate Selenium Bot with Chrome Options, returning obj webdriver.Chrome
        self.setup_chrome_options()
        bot = webdriver.Chrome(options=self.chrome_options)
        print("Creating a new session!")

        ## Check if is logged in
        while self.login_linkedin(bot=bot) != True:
            pass
        print("Login Succesfull!")
        self.my_profile_url = self.get_my_profile_url(session=bot)
        return bot

    def login_linkedin(self, bot: webdriver.Chrome):
        """Function to run the login process into linkedin"""
        # Access the website
        print("Verifying login process")
        bot.get("https://www.linkedin.com/login")

        # Check if we already have the login cookies in this session
        if "linkedin.com/feed/" in bot.current_url:
            time.sleep(0.5)
            return True

        print("Executing login script")
        # Add Delay
        time.sleep(SHORT_DELAY)

        # Locate the email and password fields
        email_field = bot.find_element(By.ID, value="username")
        password_field = bot.find_element(By.ID, value="password")
        submit_button = bot.find_element(By.CLASS_NAME, value="btn__primary--large")

        # Fill the email and password fields
        time.sleep(SHORT_DELAY)
        email_field.send_keys(self.credentials["username"])
        time.sleep(SHORT_DELAY)
        password_field.send_keys(self.credentials["password"])
        time.sleep(SHORT_DELAY)
        submit_button.click()
        time.sleep(SHORT_DELAY)

        self.login_linkedin(bot=bot)

    def get_my_profile_url(self, session: webdriver.Chrome):
        session.get("https://www.linkedin.com/in/")
        time.sleep(LONG_DELAY)
        print("Saved my profile URL")
        return session.current_url

    def scrape_save_html_file(self, session: webdriver.Chrome, page_name: str):
        session.get(f"{self.my_profile_url}/details/{page_name}")
        time.sleep(LONG_DELAY)
        html = session.page_source
        with open(
            file=f"src/html_files/{page_name}.html", mode="w"
        ) as file:
            file.write(html)
        self.logs.update_json(page_name=page_name)

    def update_routine(self, session: webdriver.Chrome):
        for page in self.pages_to_scrape:
            if self.logs.check_deadline(page_name=page, deadline_days=30):
                self.scrape_save_html_file(session=session, page_name=page)
                print(f"Page '{page}' was scrapped and saved")
        session.quit()
        return True


if __name__ == "__main__":
    linkedin_bot = LinkedinBot(credentials=CREDENTIALS)
    session = linkedin_bot.create_session()
    linkedin_bot.update_routine(session=session)
    time.sleep(30)
    linkedin_parser = LinkedinParser()
    linkedin_parser.parse_experience_page()
