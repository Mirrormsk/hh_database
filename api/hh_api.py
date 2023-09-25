from utils.safe_request import get_request_safe


class HeadHunterParser:
    def __init__(self):
        self.__api_url = "https://api.hh.ru/"
        self.user_agent = "VacancyHelperApp/0.1"
        self.__host = "hh.ru"
        # self.search_params = {}

    def _get_page_data(self, employer_id: str, page: int) -> dict:
        headers = {"HH-User-Agent": self.user_agent}
        url = self.__api_url + "vacancies"
        params = {
            "employer_id": employer_id,
            "host": self.__host,
            "page": page,
            "per_page": 100,
            # "period": 7,
            # "schedule": "remote",
            "only_with_salary": False,
        }
        response = get_request_safe(url=url, headers=headers, params=params)
        return response.json()

    def get_vacancies_by_employer(self, employer_id: str) -> list[dict]:
        first_page = self._get_page_data(employer_id, 0)

        items: list = first_page["items"]

        total_pages = first_page["pages"]

        if total_pages > 1:

            for page in range(1, total_pages):
                page_items = self._get_page_data(employer_id, page)["items"]
                items.extend(page_items)

        return items


if __name__ == "__main__":
    api = HeadHunterParser()

    hh_vacancies = api.get_vacancies_by_employer("1455")

    print(len(hh_vacancies))
