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
        return str(document)

    def find_bullet_points(doc_json: str):
        bullet_points = {}

        # Traverse the nested JSON structure to find bullet points
        # This is just a conceptual example; you'll need to adapt this
        # to the actual structure of your Google Docs JSON.

        for element in doc_json.get("body", {}).get("content", []):
            if "paragraph" in element:
                # Assuming bullet points have a specific style or metadata
                if element["paragraph"].get("bullet", {}).get("glyphSymbol") == "●":
                    text_elements = element["paragraph"]["elements"]
                    text_content = "".join(
                        [e["textRun"]["content"] for e in text_elements]
                    )

                    # Do something with the text content of the bullet point
                    # For example, store it in a dictionary
                    position = (
                        "some_position"  # Replace with actual position identifier
                    )
                    if position in bullet_points:
                        bullet_points[position].append(text_content)
                    else:
                        bullet_points[position] = [text_content]

        return bullet_points

    def parse_standard_resume(self, doc_content: str) -> Dict[str, str]:
        """Parses the standard resume to identify job roles and their bullet points."""

        # Initialize an empty dictionary to hold job roles and their bullet points
        roles_dict = {}

        # Split the resume content by lines
        lines = doc_content.split("\n")

        # Initialize variables to hold the current job role and its bullet points
        current_role = None
        bullet_points = []

        # Loop through each line to identify job roles and bullet points
        for line in lines:
            # Check if the line could be a job role (e.g., it contains a date range)
            role_match = re.search(r"\b\d{4}\s*[-–]\s*\d{4}\b", line)
            if role_match:
                # Save the previous job role and its bullet points to the dictionary
                if current_role:
                    roles_dict[current_role] = bullet_points

                # Update the current job role and clear the bullet points list
                current_role = line.strip()
                bullet_points = []
            elif line.startswith("-"):
                # This line is a bullet point; add it to the list
                bullet_points.append(line.strip())

        # Save the last job role and its bullet points to the dictionary
        if current_role:
            roles_dict[current_role] = bullet_points

        return roles_dict


standard_id = os.environ.get("STANDARD_TEMPLATE_ID")

google = GoogleDocsManager()
google.authenticate()
standard_doc = google.read_doc(standard_id)
dics = google.find_bullet_points(standard_doc)
print(dics)
