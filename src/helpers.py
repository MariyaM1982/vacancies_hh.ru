from typing import Dict, List

from src.vacancy import Vacancy


def format_salary(salary: str) -> str:
    # Преобразуем строку в число
    number = int(salary)
    # Форматируем число с разделителем тысяч
    return "{:,}".format(number).replace(",", " ")


def print_vacancies(vacancies: list) -> None:
    for vacancy in vacancies:
        try:
            print(f"Название: {vacancy.name}")
            print(f"Зарплата: {vacancy.salary}")
            print(f"Ссылка: {vacancy.url}")
            print(f"Описание: {vacancy.description[:100]}...")
            print("-" * 40)
        except Exception as e:
            print(f"Ошибка при выводе вакансии: {e}")


def sort_vacancies_by_salary(vacancies: list) -> list:
    def get_salary(vacancy):
        try:
            # Извлекаем числовое значение зарплаты
            salary_str = vacancy.salary
            if "Не указана" in salary_str:
                return -1

            # Ищем первое число в строке зарплаты
            import re

            numbers = re.findall(r"\d+", salary_str)
            if numbers:
                return int(numbers[0].replace(" ", ""))
            return -1
        except Exception:
            return -1

    return sorted(vacancies, key=get_salary, reverse=True)
