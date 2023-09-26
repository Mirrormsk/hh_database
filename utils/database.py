import psycopg2
from psycopg2.extensions import cursor
from psycopg2.extras import execute_values
from pydantic import BaseModel

from utils.currency_update import get_current_rates


def create_database(database_name: str, params: dict) -> None:
    """Creating database with 'employers' and 'vacancies' tables"""
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
                    name VARCHAR NOT NULL,
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

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE currency (
                    char_code CHAR(3) PRIMARY KEY,
                    value FLOAT NOT NULL,
                    name VARCHAR(100) NOT NULL
                )
            """
            )
    conn.close()


def get_fieldnames(model: BaseModel):
    """Returns fieldnames of model"""
    return f"({', '.join(key for key in model.model_dump().keys())})"


def get_values(model: BaseModel):
    """Returns string representation for tuple with model values"""
    return tuple(model.model_dump().values())


def insert_model(table_name: str, cur: cursor, model: BaseModel):
    """Insert one model to database"""
    # Making string with fieldnames
    fieldnames = get_fieldnames(model)

    # Making model values tuple
    model_values = get_values(model)

    # Generating query
    query = f"INSERT INTO {table_name} {fieldnames} VALUES ({', '.join(['%s'] * len(model_values))})"

    # Executing query
    cur.execute(query, model_values)


def insert_models_array(table_name: str, cur: cursor, models_array: list[BaseModel]):
    """
    Insert array of models to database.
    Uses new fastest 'execute_values' method (from psycopg2 2.7).
    """
    if models_array:
        # Getting fieldnames for insert
        fieldnames = get_fieldnames(models_array[0])

        # Uses set because hh.ru sometimes gives one vacancy on two different pages ¯\_(ツ)_/¯
        values = set(get_values(model) for model in models_array)

        # Generating query
        query = f"INSERT INTO {table_name} {fieldnames} VALUES %s"

        # Executing query
        execute_values(cur, query, values)
    else:
        raise ValueError("Models array can't be empty")


def update_currency_table(database_name: str, cur: cursor):
    """Updates exchange rates"""

    rates_data = get_current_rates()

    rates = [
        (
            "BYR" if name == "BYN" else name,
            value["Value"] / value["Nominal"],
            value["Name"],
        )
        for name, value in rates_data.items()
    ]

    query = f"INSERT INTO currency (char_code, value, name) VALUES %s"
    cur.execute("INSERT INTO currency VALUES ('RUR', 1, 'Российский рубль')")

    execute_values(cur, query, rates)
