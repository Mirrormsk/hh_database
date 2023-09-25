import psycopg2


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