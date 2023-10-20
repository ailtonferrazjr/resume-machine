import json
from datetime import datetime, timedelta

LOG_PATH = "resume_machine/src/html_files/scrapping_logs.json"
JSON_TEMPLATE = {
    "experience": str(datetime.min),
    "education": str(datetime.min),
    "skills": str(datetime.min),
}


class ScrappingLogs:
    def __init__(self):
        self.log_path = LOG_PATH
        self.data = self.read_or_create_json(LOG_PATH)

    # 1. Read or create JSON file
    def read_or_create_json(self, file_path):
        """Function to create or read a json fale, input should be the file path"""
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                print("Log file was found!")
        except FileNotFoundError:
            print("Log file was not found, creating one")
            data = JSON_TEMPLATE
            with open(file_path, "w") as f:
                json.dump(data, f)
        return data

    # 2. Check if deadline is exceeded
    def check_deadline(self, page_name: str, deadline_days: int):
        """Function to check if the last time that page was scrapped was more than X days ago"""
        last_scraped_date = datetime.fromisoformat(self.data[page_name])
        deadline_date = last_scraped_date + timedelta(days=deadline_days)
        return datetime.now() > deadline_date

    # 3. Update JSON file
    def update_json(self, page_name):
        with open(self.log_path, "r") as f:
            data = json.load(f)
        data[page_name] = str(datetime.now())
        with open(self.log_path, "w") as f:
            json.dump(data, f)
            print(f"New log saved for page '{page_name}'")
        self.data = self.read_or_create_json(self.log_path)
