from utils import get_request_safe


class HeadHunterParser:
    def __init__(self):
        self.__api_url = "https://api.hh.ru/"
        self.__user_agent = "VacancyHelperApp/1.0"
        self.__host = "hh.ru"
        self.__headers = {"HH-User-Agent": self.__user_agent}
        # self.search_params = {}

    def _get_vacancies_page_data(self, employer_id: str, page: int) -> dict:
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
        response = get_request_safe(url=url, headers=self.__headers, params=params)

        return response.json()

    def get_vacancies_by_employer(self, employer_id: str) -> list[dict]:
        first_page = self._get_vacancies_page_data(employer_id, 0)

        items: list = first_page["items"]

        total_pages = first_page["pages"]

        if total_pages > 1:

            for page in range(1, total_pages):
                page_items = self._get_vacancies_page_data(employer_id, page)["items"]
                items.extend(page_items)

        return items

    def get_employer_info(self, employer_id: str):
        """Method takes information about employer and returns as a dict"""
        request_url = f"{self.__api_url}employers/{employer_id}"

        response = get_request_safe(url=request_url, headers=self.__headers)

        if response.status_code == 404:
            raise ValueError(f"Работодатель с id {employer_id} не найден")

        return response.json()

    def set_user_agent(self, new_user_agent: str) -> None:
        """
        Method changes HH-User-Agent parameter.
        It may be useful when changing the name of the application.
        """
        self.__user_agent = new_user_agent


if __name__ == "__main__":
    api = HeadHunterParser()

    hh_vacancies = api.get_employer_info("1455")

    print(len(hh_vacancies))
    print(hh_vacancies)
