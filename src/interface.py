import psycopg2

from config import config
from src.create_db import create_data_base, save_data_to_db
from src.db_manager import DBManager
from src.hh_api import get_vacancies, get_companies, get_vacancy_list

params = config()
data = get_vacancies(get_companies())
vacancies = get_vacancy_list(data)

create_data_base("top_vacancies", params)
conn = psycopg2.connect(dbname="top_vacancies", **params)
save_data_to_db(vacancies, "top_vacancies", params)

def show_interfaсe():
    """
    Функция для взаимодействия с пользователем
    """
    db_manager = DBManager("top_vacancies", params)
    print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          f"3 - Средняя зарплата по вакансиям\n"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n")
    user_answer = input("Введите номер запроса\n")
    if user_answer == "1":
        print(f"Список всех компаний и количество вакансий у каждой компании:")
        for key, item in db_manager.get_companies_and_vacancies_count().items():
            print(f"{key} - {item} вакансий")
    elif user_answer == "2":
        all_vacancies = db_manager.get_all_vacancies()
        print(f"Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию:\n")
        for vac in all_vacancies:
            print(f"{', '.join(str(x) for x in vac)}")
    elif user_answer == "3":
        avg_salary = db_manager.get_avg_salary()
        print(f"Средняя зарплата по вакансиям:\n")
        for item in avg_salary:
            for salary in item:
                print(f"{salary:.2f}")
    elif user_answer == "4":
        vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
        print(f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям: {vacancies_with_higher_salary}\n")
        for vac in vacancies_with_higher_salary:
            print(f"{vac[0]} - {vac[1]}")
    elif user_answer == "5":
        user_input = input(f'Введите слово: ')
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
        print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово:\n")
        for vac in vacancies_with_keyword:
            print(f"{', '.join(str(x) for x in vac)}")
    else:
        print("Введен неверный запрос")
