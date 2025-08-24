from typing import Dict, List

from src.vacancy import Vacancy


def format_salary(salary_str: str) -> str:
    """Форматирует строку с зарплатой"""
    if "не указана" in salary_str.lower():
        return salary_str
    # Добавляем пробелы для лучшей читаемости
    return " ".join([salary_str[i : i + 3] for i in range(0, len(salary_str), 3)])


def print_vacancy(vacancy: Vacancy) -> None:
    """Красиво выводит вакансию в консоль"""
    print(f"Название: {vacancy.name}")
    print(f"Зарплата: {format_salary(vacancy.salary)}")
    print(f"Ссылка: {vacancy.url}")
    print(f"Описание: {vacancy.description[:100]}...")
    print("-" * 40)


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Выводит список вакансий"""
    for vacancy in vacancies:
        print_vacancy(vacancy)


def sort_vacancies_by_salary(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по зарплате"""
    return sorted(
        vacancies,
        key=lambda x: (
            int(x.salary.replace(" ", "")) if x.salary != "Зарплата не указана" else 0
        ),
        reverse=True,
    )
