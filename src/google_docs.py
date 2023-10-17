from typing import Dict
import dotenv, os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import re

dotenv.load_dotenv()
credentials = os.environ.get("GOOGLE_KEY")
print(credentials)


class GoogleDocsManager:
    def __init__(self):
        self.credentials_path = "resume_machine/credentials/google_config.json"
        self.credentials = None
        self.standard_id = os.environ.get("STANDARD_TEMPLATE_ID")

    def authenticate(self) -> None:
        self.credentials = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=[
                "https://www.googleapis.com/auth/documents",
                "https://www.googleapis.com/auth/drive",
            ],
        )

    def read_doc(self, doc_id: str) -> str:
        """Reads a Google Doc and returns its content."""

        # Build the Google Docs API client
        docs_service = build("docs", "v1", credentials=self.credentials)

        # Fetch the Google Doc
        document = docs_service.documents().get(documentId=doc_id).execute()

        # For now, we'll just return the entire document object as a string
        return document

    def parse_doc(self, docs) -> Dict:
        job_positions_dict = {}  # Dictionary to store each job position and its bullet points
        current_job_title = None  # To store the current job title
        current_bullet_points = []  # To store bullet points for the current job
        collecting = False  # Flag to start/stop collecting bullet points

        # Loop through the JSON content
        for item in docs['body']['content']:
            if 'paragraph' in item:
                elements = item['paragraph']['elements']
                
                for element in elements:
                    if 'textRun' in element:
                        content = element['textRun']['content'].strip()
                        bold = element['textRun']['textStyle'].get('bold', False)
                        
                        if "PROFESSIONAL EXPERIENCE" in content:
                            collecting = True  # Start collecting after "PROFESSIONAL EXPERIENCE"
                        elif "EDUCATION" in content:
                            collecting = False  # Stop collecting after "EDUCATION"

                        if collecting:
                            if bold:  # If we find bold text, it's a new job title
                                # If there's a current job, add it to job_positions_dict
                                if current_job_title:
                                    job_positions_dict[current_job_title] = current_bullet_points
                                    current_bullet_points = []
                                
                                current_job_title = content  # Set the new job title
                                
                            elif "bullet" in item['paragraph']:  # If we find a bullet point
                                current_bullet_points.append(content)  # Add the bullet point to the current job

        # Add the last job if it exists
        if current_job_title and current_bullet_points:
            job_positions_dict[current_job_title] = current_bullet_points

        return job_positions_dict
    
google = GoogleDocsManager()
google.authenticate()
standard_doc = google.read_doc(google.standard_id)
dics = google.parse_doc(docs=standard_doc)
print(dics)
# with open("docs.json", mode="w") as file:
#     file.write(standard_doc)
