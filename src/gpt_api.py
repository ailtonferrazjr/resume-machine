import openai
import requests
import os, dotenv
from chatgptmax import send


dotenv.load_dotenv()


class CHATGPT:
    def __init__(self):
        self.gpt = openai
        self.gpt.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"

    def send_html(html):
        text = "Hey, i need to parse down a HTML file (which comes from linkedin), in order to find the following information about which company i've worked and return it as structured data"
        text += "Each position should have: company, job title, start_date, end_date, description and skills\n"
        text += "Please lookup in the HTML that i'm sending, in order to find and fullfill this dict, can you do it?"
        text += "Also, please reply me only the JSON object itself, nothing else, so I can use it directly in my code and with no breaklines as 'slash n' or trimmed spaces it has to be clean data"
        text += "Dont add any information that is missing like apologies or anything else, i want the JSON you can extract and thats it"
        responses = send(
            prompt=text,
            text_data=html,
            chat_model="gpt-3.5-turbo",
            model_token_limit=4097,
            max_tokens=1057,
        )

        return responses
