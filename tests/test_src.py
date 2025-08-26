import io
import os
import sys
import unittest

from src.helpers import (
    format_salary,
    print_vacancies,
    print_vacancy,
    sort_vacancies_by_salary,
)
from src.json_storage import JSONStorage
from src.vacancy import Vacancy


class TestJSONStorage(unittest.TestCase):
    def setUp(self):
        self.storage = JSONStorage("test_vacancies.json")
        self.test_vacancy = {
            "name": "Тестовая вакансия",
            "url": "http://test.com",
            "salary": "100000",
            "description": "Тестовое описание",
        }
        if os.path.exists("test_vacancies.json"):
            os.remove("test_vacancies.json")

    def test_add_vacancy(self):
        self.storage.add_vacancy(self.test_vacancy)
        self.assertIn(self.test_vacancy, self.storage.get_vacancies())

    def test_add_duplicate(self):
        self.storage.add_vacancy(self.test_vacancy)
        self.storage.add_vacancy(self.test_vacancy)
        vacancies = self.storage.get_vacancies()
        self.assertEqual(len(vacancies), 1)

    def test_delete_vacancy(self):
        self.storage.add_vacancy(self.test_vacancy)
        self.assertTrue(self.storage.delete_vacancy(self.test_vacancy["url"]))
        self.assertNotIn(self.test_vacancy, self.storage.get_vacancies())

    def tearDown(self):
        if os.path.exists("test_vacancies.json"):
            os.remove("test_vacancies.json")


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.vacancy = Vacancy(
            name="Тестировщик",
            url="http://test.com",
            salary="100000",
            description="Тестовый описание",
        )
        self.vacancies = [
            Vacancy(
                name="Python Dev", salary="200000", url="url1", description="Python"
            ),
            Vacancy(name="Java Dev", salary="150000", url="url2", description="Java"),
            Vacancy(name="JS Dev", salary="180000", url="url3", description="JS"),
            Vacancy(
                name="No Salary",
                salary="Зарплата не указана",
                url="url4",
                description="No Salary",
            ),
        ]

    def test_format_salary(self):
        self.assertEqual(format_salary("100000"), "100 000")
        self.assertEqual(format_salary("Зарплата не указана"), "Зарплата не указана")
        self.assertEqual(format_salary("2000000"), "2 000 000")
        self.assertEqual(format_salary("50000"), "50 000")

    def test_sort_vacancies(self):
        sorted_vacancies = sort_vacancies_by_salary(self.vacancies)
        expected_salaries = ["200000", "180000", "150000", "Зарплата не указана"]
        actual_salaries = [v.salary for v in sorted_vacancies]
        self.assertEqual(actual_salaries, expected_salaries)

    def test_print_vacancy(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        print_vacancy(self.vacancy)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertIn("Тестировщик", output)
        self.assertIn("100 000", output)
        self.assertIn("http://test.com", output)
        self.assertIn("Тестовый описание", output)

    def test_print_vacancies(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        print_vacancies(self.vacancies)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        for vacancy in self.vacancies:
            self.assertIn(vacancy.name, output)


class TestVacancyModel(unittest.TestCase):
    def test_vacancy_creation(self):
        vacancy = Vacancy(
            name="Тестировщик",
            url="http://test.com",
            salary="100000",
            description="Тестовый описание",
        )
        self.assertEqual(vacancy.name, "Тестировщик")
        self.assertEqual(vacancy.url, "http://test.com")
        self.assertEqual(vacancy.salary, "100000")
        self.assertEqual(vacancy.description, "Тестовый описание")

    def test_salary_validation(self):
        vacancy_with_salary = Vacancy(
            name="Тестировщик",
            url="http://test.com",
            salary="100000",
            description="Тестовый описание",
        )
        self.assertEqual(vacancy_with_salary.salary, "100000")

        vacancy_without_salary = Vacancy(
            name="Тестировщик",
            url="http://test.com",
            salary="",
            description="Тестовый описание",
        )
        self.assertEqual(vacancy_without_salary.salary, "Зарплата не указана")

    def test_comparison(self):
        vacancy1 = Vacancy(
            name="Тестировщик",
            url="http://test.com",
            salary="100000",
            description="Тестовый описание",
        )
        vacancy2 = Vacancy(
            name="Тестировщик",
            url="http://test.com",
            salary="100000",
            description="Тестовый описание",
        )
        vacancy3 = Vacancy(
            name="Тестировщик",
            url="http://test.com",
            salary="150000",
            description="Тестовый описание",
        )

        self.assertTrue(vacancy1 == vacancy2)
        self.assertFalse(vacancy1 == vacancy3)
        self.assertTrue(vacancy1 < vacancy3)

    def test_to_dict(self):
        vacancy = Vacancy(
            name="Тестировщик",
            url="http://test.com",
            salary="100000",
            description="Тестовый описание",
        )
        expected_dict = {
            "name": "Тестировщик",
            "url": "http://test.com",
            "salary": "100000",
            "description": "Тестовый описание",
        }
        self.assertEqual(vacancy.to_dict(), expected_dict)
