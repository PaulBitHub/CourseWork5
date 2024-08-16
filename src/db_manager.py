import psycopg2


class DBManager:
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self, database_name, params) -> None:
        """При создании - параметры для всех объектов класса"""
        self.dbname = database_name
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def execute_query(self, query, params=None) -> list:
        """Универсальный метод для выполнения запроса и получения результатов"""
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def close(self) -> None:
        """Закрытие соединения с базой данных"""
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> dict:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        query = """
        SELECT companies.company_name, COUNT(vacancies.company_id)
        FROM companies
        JOIN vacancies USING (company_id)
        GROUP BY companies.company_name
        ORDER BY COUNT DESC
        """
        rows = self.execute_query(query)
        return {row[0]: row[1] for row in rows}

    def get_all_vacancies(self) -> list:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты, ссылки на вакансию
        """
        query = """
        SELECT company_name, job_title, salary_from, currency, link_to_vacancy 
        FROM vacancies
        """
        return self.execute_query(query)

    def get_avg_salary(self) -> list | None:
        """Возвращает среднюю зарплату по вакансиям из БД"""
        query = "SELECT AVG(salary_from) FROM vacancies"
        rows = self.execute_query(query)
        return rows if rows else None

    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям в БД"""
        query = """
        SELECT job_title, salary_from 
        FROM vacancies
        WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
        """
        return self.execute_query(query)

    def get_vacancies_with_keyword(self, keyword) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например 'python'
        """
        query = """SELECT company_name, job_title, salary_from, experience, requirement FROM vacancies WHERE LOWER(job_title) LIKE %s"""
        return self.execute_query(query, ('%' + keyword.lower() + '%',))
