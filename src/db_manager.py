import psycopg2


class DBManager:
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self, database_name, params):
        """При создании - параметры для всех объектов класса"""
        self.dbname = database_name
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def execute_query(self, query, params=None):
        """Универсальный метод для выполнения запроса и получения результатов"""
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def close(self):
        """Закрытие соединения с базой данных"""
        self.cur.close()
        self.conn.close()


class VacancyService:
    """Класс для работы с данными о вакансиях"""

    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def get_companies_and_vacancies_count(self) -> dict:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        query = """
        SELECT company_name, COUNT(*) 
        FROM vacancies
        GROUP BY company_name
        """
        rows = self.db_manager.execute_query(query)
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
        return self.db_manager.execute_query(query)

    def get_avg_salary(self):
        """Возвращает среднюю зарплату по вакансиям из БД"""
        query = "SELECT AVG(salary_from) FROM vacancies"
        rows = self.db_manager.execute_query(query)
        return rows if rows else None

    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям в БД"""
        query = """
        SELECT job_title, salary_from 
        FROM vacancies
        WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
        """
        return self.db_manager.execute_query(query)

    def get_vacancies_with_keyword(self, keyword) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например 'python'
        """
        query = """SELECT * FROM vacancies WHERE LOWER(job_title) LIKE %s"""
        return self.db_manager.execute_query(query, ('%' + keyword.lower() + '%',))
