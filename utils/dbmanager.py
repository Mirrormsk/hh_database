import os.path
from typing import Any

from config import config
import psycopg2


class DBManager:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.params = config(filename=os.path.join("..", "database.ini"))
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)

    def execute_query(self, query: str) -> list[tuple[Any]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

        except Exception as ex:
            print("Ошибка запроса")

        finally:
            self.conn.close()

    def get_companies_and_vacancies_count(self) -> list[tuple[Any]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        query = """
                SELECT e.name, count(*) as total_vacancies FROM vacancies v
                JOIN employers e
                    ON v.employer_id = e.id
                GROUP BY e.name;
                """
        return self.execute_query(query)

    def get_all_vacancies(self) -> list[tuple[Any]]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        Отсортировано по убыванию минимальной зарплаты.
        """
        query = """
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.salary_currency, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                LEFT JOIN currency c ON v.salary_currency = c.char_code
                WHERE v.salary_from IS NOT NULL
                ORDER BY v.salary_from * c.value DESC
                """
        return self.execute_query(query)

    def get_avg_salary(self):
        query = """
                SELECT (AVG(salary_from) + AVG(salary_to)) / 2 AS avg_salary
                FROM vacancies
                """
        return round(self.execute_query(query)[0][0])

    def get_vacancies_with_higher_salary(self):
        query = """
                 SELECT *
                 FROM vacancies
                 WHERE salary_from > (
                     SELECT (AVG(salary_from) + AVG(salary_to)) / 2 AS avg_salary
                     FROM vacancies)
                     OR
                     salary_to > (
                     SELECT (AVG(salary_from) + AVG(salary_to)) / 2 AS avg_salary
                     FROM vacancies)
               """
        return self.execute_query(query)

    def get_vacancies_with_keyword(self, keyword: str):
        query = f"""SELECT *
                   FROM vacancies v
                   WHERE v.name ILIKE '%{keyword}%'"""
        return self.execute_query(query)