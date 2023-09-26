import psycopg2
from tqdm import tqdm

from api.hh_api import HeadHunterParser
from config import config
from models.models import Employer, Vacancy
from utils.database import (create_database,
                            insert_model,
                            insert_models_array,
                            update_currency_table)

DATABASE_NAME = "headhunter"

# API interface initial
api = HeadHunterParser()

# Favorites list
favorites = {
    "Skyeng": 1122462,
    "Сбербанк": 3529,
    "Яндекс": 1740,
    "Ozon": 2180,
    "Тинькоф": 78638,
    "МТС": 3776,
    "Билайн": 4934,
    "Лабаратория Касперского": 1057,
    "VK": 15478,
    "Selectel": 633069,
    "Контур": 41862,
}


def main():

    # Database creation
    params = config()
    create_database(DATABASE_NAME, params)

    conn = psycopg2.connect(dbname=DATABASE_NAME, **params)
    with conn.cursor() as cur:

        # Updating currency table
        update_currency_table(DATABASE_NAME, cur)

        # Start to pull data from api
        for employer_name, employer_id in tqdm(favorites.items(), desc="Loading data"):

            try:
                # Get company info from api
                data = api.get_employer_info(employer_id)

                # Validation and model creation
                employer = Employer.model_validate(data)

                # Insert company info into table employers
                insert_model("employers", cur, employer)
                conn.commit()

                # Getting company vacancies
                vacancies_data = api.get_vacancies_by_employer(employer_id)

                # List for Vacancy models
                vacancies = []

                # Validate each vacancies separately
                for vacancy in vacancies_data:
                    try:
                        vacancy_obj = Vacancy.model_validate(vacancy)
                        vacancies.append(vacancy_obj)
                    except Exception as ex:
                        print(f"Error in vacancy:")
                        print(vacancy)
                        print(f"Error message:\n{ex}")

                # Inserting into database
                insert_models_array("vacancies", cur, vacancies)

            except Exception as ex:
                print(f"Ошибка получения данных по работодателю {employer_name}")
                print(ex)
            else:
                conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
