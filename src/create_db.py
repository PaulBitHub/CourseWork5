import psycopg2


def create_data_base(database_name, params) -> None:
    """
   Создание базы данных и таблиц с данными о компаниях и вакансиях
    """

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True

    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            # Создание таблицы companies с первичным ключом
            cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR(255),
            company_url TEXT
            )
            """)

        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INT,
                company_name VARCHAR(255),
                job_title VARCHAR,
                link_to_vacancy TEXT,
                salary_from INT,
                currency VARCHAR(20),
                experience TEXT,
                description TEXT,
                requirement TEXT,
                FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
            )
            """)
    conn.commit()
    conn.close()


def save_data_to_db(data, database_name, params) -> None:
    """
    Заполнение таблиц companies и vacancies данными
    """
    insert_company_q = """
           INSERT INTO companies (company_name, company_url) VALUES (%s, %s) RETURNING company_id
       """
    insert_vacancy_q = """
           INSERT INTO vacancies (company_id, company_name, job_title, link_to_vacancy, salary_from, currency, experience, description,
                                  requirement)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
       """
    select_company_q = """
           SELECT company_id FROM companies WHERE company_name = %s AND company_url = %s
       """

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            for vacancy in data:
                # Проверяем, существует ли компания в базе данных
                cur.execute(select_company_q, (vacancy['company_name'], vacancy['company_url']))
                company_id = cur.fetchone()

                # Если компания уже существует, берем ее ID
                if company_id:
                    company_id = company_id[0]
                # Если компании нет, вставляем ее и получаем ID
                else:
                    cur.execute(insert_company_q, (vacancy['company_name'], vacancy['company_url']))
                    company_id = cur.fetchone()[0]

                # Теперь вставляем вакансию с company_id и company_name
                cur.execute(insert_vacancy_q, (company_id, vacancy['company_name'], vacancy['job_title'], vacancy['link_to_vacancy'],
                                               vacancy['salary_from'], vacancy['currency'],
                                               vacancy["experience"], vacancy['description'],
                                               vacancy['requirement']))
    conn.commit()
    conn.close()
