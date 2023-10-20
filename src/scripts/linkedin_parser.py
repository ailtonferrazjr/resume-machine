from bs4 import BeautifulSoup
import re
import json
import calendar

MONTHS = [calendar.month_abbr[i] + " 20" for i in range(1, 13)]


class LinkedinParser:
    """Class created for the methods of parsing the specific types of pages from Linkedin"""

    def __init__(self):
        pass

    def load_soup(self, page_name: str) -> BeautifulSoup:
        self.page_name = page_name
        with open(
            file=f"resume_machine/src/html_files/{page_name}.html", mode="r"
        ) as file:
            return BeautifulSoup(file, "html.parser")

    def parse_experience(self, soup: BeautifulSoup):
        elements = soup.find_all(
            name="li",
            class_="pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column",
        )
        return elements

    def parse_visually_hidden(self, element: BeautifulSoup):
        hidden_elements = element.find_all(name="span", class_="visually-hidden")
        hidden_list = [
            hidden.getText().replace("\n", "").strip() for hidden in hidden_elements
        ]
        treated_list = [
            re.sub(" +", " ", hidden_list[_]) for _ in range(len(hidden_list))
        ]
        return treated_list

    def find_period_of_time(self, hidden_list: list) -> list:
        time_list = []
        for _ in range(len(hidden_list)):
            for month in MONTHS:
                if month in hidden_list[_]:
                    time_list.append(_)
                    break
        return time_list

    def parse_company(self, hidden_list: list, period_of_time_list: list) -> dict:
        total_positions = len(period_of_time_list)

        if total_positions == 0:
            return

        company_name = hidden_list[0]
        company_dict = {company_name: []}

        for _ in range(total_positions):
            position_dict = {
                "job_name": hidden_list[period_of_time_list[_] - 1],
                "period": hidden_list[period_of_time_list[_]],
                "job_location": hidden_list[period_of_time_list[_] + 1],
                "description": hidden_list[period_of_time_list[_] + 2],
                "skills": hidden_list[period_of_time_list[_] + 3],
            }

            company_dict[company_name].append(position_dict)

        return company_dict

    def parse_experience_page(self) -> str:
        experience_page = self.load_soup("experience")
        target_elements = self.parse_experience(experience_page)
        experiences_list = []
        for el in target_elements:
            hidden_list = self.parse_visually_hidden(element=el)
            period_of_time_list = self.find_period_of_time(hidden_list=hidden_list)
            company = self.parse_company(
                hidden_list=hidden_list, period_of_time_list=period_of_time_list
            )
            if company is not None:
                experiences_list.append(company)

        experiences_json = json.dumps(experiences_list, ensure_ascii=False)
        self.save_to_db(page_name=self.page_name, json=experiences_json)

    def save_to_db(self, page_name: str, json: str):
        with open(
            f"resume_machine/src/html_files/json_files/{page_name}.json", mode="w"
        ) as file:
            file.write(json)


if __name__ == "__main__":
    lid = LinkedinParser()
    experiences_dic = lid.parse_experience_page()
