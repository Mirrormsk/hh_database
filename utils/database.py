import psycopg2

from psycopg2.extras import execute_values
from pydantic import BaseModel


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения каналов и видео"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    open_vacancies INT,
                    area VARCHAR(100),
                    url VARCHAR,
                    description TEXT
                )
            """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL
                    employer_id INT REFERENCES employers(id),
                    area VARCHAR(100),
                    salary_from INT,
                    salary_to INT,
                    salary_currency VARCHAR(5),
                    url VARCHAR,
                    requirement TEXT,
                    responsibility TEXT
                )
            """
            )
    conn.close()


def get_fieldnames(model: BaseModel):
    return f"({', '.join(key for key in model.model_dump().keys())})"


def get_values(model: BaseModel):
    return str(tuple(model.model_dump().values()))


def insert_model(table_name: str, cur: psycopg2.cursor, model: BaseModel):

    # Making string with fieldnames
    fieldnames = get_fieldnames(model)

    # Making model values tuple
    model_values = get_values(model)

    # Generating query
    query = f"INSERT INTO {table_name} {fieldnames} VALUES %s"

    # Executing query
    cur.execute(query, model_values)


def insert_models_array(
    table_name: str, cur: psycopg2.cursor, models_array: list[BaseModel]
):
    if models_array:
        fieldnames = get_fieldnames(models_array[0])

        values = [get_values(model) for model in models_array]

        query = f"INSERT INTO {table_name} {fieldnames} VALUES %s"

        # Executing query
        execute_values(cur, query, values)
