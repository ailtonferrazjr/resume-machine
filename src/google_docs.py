from typing import Dict
import dotenv, os
from google.oauth2.service_account import Credentials


dotenv.load_dotenv()
credentials = os.environ.get("GOOGLE_KEY")
print(credentials)


class GoogleDocsManager:
    def __init__(self, credentials: Dict):
        self.credentials_path = ""
        self.client = None

    def authenticate(self) -> None:
        # TODO: Authenticate with Google API
        pass

    def read_doc(self, doc_id: str) -> str:
        # TODO: Read Google Doc
        pass

    def parse_doc(self, doc_content: str) -> Dict[str, str]:
        # TODO: Parse Google Doc to identify placeholders and sections
        pass
