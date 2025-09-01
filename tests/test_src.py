import io
import os
import json
import sys
import unittest
from io import StringIO
from typing import Dict, List
from unittest.mock import MagicMock
from poetry.console.commands import self

from src.helpers import (
    format_salary,
    print_vacancies,
    sort_vacancies_by_salary,
)
from src.json_storage import JSONStorage
from src.vacancy import Vacancy
from src.base_storage import BaseStorage


class TestJSONStorage(unittest.TestCase):
        def setUp(self):

            # Создаем временный файл в текущей директории
            self.temp_file = "test_vacancies.json"
            self.storage = JSONStorage(self.temp_file)

            self.test_vacancy = {
                "name": "Тестовая вакансия",
                "url": "https://test.com",
                "salary": "100000",
                "description": "Описание",
            }
            self.test_vacancy2 = {
                "name": "Вторая вакансия",
                "url": "https://test2.com",
                "salary": "150000",
                "description": "Другое описание",
            }

        def tearDown(self):
            # Удаляем файл после тестов
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)

        def test_add_vacancy(self):
            self.storage.add_vacancy(self.test_vacancy)
            vacancies = self.storage.get_vacancies()
            self.assertEqual(len(vacancies), 1)
            self.assertEqual(vacancies[0], self.test_vacancy)

        def test_add_duplicate(self):
            self.storage.add_vacancy(self.test_vacancy)
            self.storage.add_vacancy(self.test_vacancy)
            vacancies = self.storage.get_vacancies()
            self.assertEqual(len(vacancies), 1)

        def test_delete_vacancy(self):
            self.storage.add_vacancy(self.test_vacancy)
            self.storage.add_vacancy(self.test_vacancy2)

            vacancies = self.storage.get_vacancies()
            self.assertEqual(len(vacancies), 2)

            result = self.storage.delete_vacancy(self.test_vacancy["url"])
            self.assertTrue(result)

            vacancies = self.storage.get_vacancies()
            self.assertEqual(len(vacancies), 1)
            self.assertEqual(vacancies[0], self.test_vacancy2)

            result = self.storage.delete_vacancy("несуществующий_url")
            self.assertFalse(result)

        def test_get_vacancies(self):
            self.storage.add_vacancy(self.test_vacancy)
            vacancies = self.storage.get_vacancies()
            self.assertEqual(len(vacancies), 1)
            self.assertEqual(vacancies[0], self.test_vacancy)

        def test_empty_file(self):
            vacancies = self.storage.get_vacancies()
            self.assertEqual(len(vacancies), 0)

        def test_multiple_additions(self):
            for i in range(5):
                vacancy = {
                    "name": f"Вакансия {i}",
                    "url": f"https://test{i}.com",
                    "salary": str(100000 + i * 10000),
                    "description": f"Описание {i}",
                }
                self.storage.add_vacancy(vacancy)

            vacancies = self.storage.get_vacancies()
            self.assertEqual(len(vacancies), 5)


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
        self.assertEqual(format_salary("2000000"), "2 000 000")
        self.assertEqual(format_salary("200000"), "200 000")
        self.assertEqual(format_salary("123456789"), "123 456 789")
        self.assertEqual(format_salary("1000"), "1 000")
        self.assertEqual(format_salary("999"), "999")

    def test_sort_vacancies(self):
        sorted_vacancies = sort_vacancies_by_salary(self.vacancies)
        expected_salaries = ["200000", "180000", "150000", "Зарплата не указана"]
        actual_salaries = [v.salary for v in sorted_vacancies]
        self.assertEqual(actual_salaries, expected_salaries)

    def test_print_vacancies(self):
        capturedOutput: StringIO = io.StringIO()
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


class TestVacancy(unittest.TestCase):
    def setUp(self):
        self.vacancy_data = {
            "name": "Python Developer",
            "url": "https://example.com",
            "salary": "100000",
            "description": "Опытный разработчик"
        }
        self.vacancy = Vacancy(**self.vacancy_data)

    def test_init_with_valid_data(self):
        self.assertEqual(self.vacancy.name, "Python Developer")
        self.assertEqual(self.vacancy.url, "https://example.com")
        self.assertEqual(self.vacancy.salary, "100000")
        self.assertEqual(self.vacancy.description, "Опытный разработчик")

    def test_init_with_empty_values(self):
        empty_vacancy = Vacancy("", "", "", "")
        self.assertEqual(empty_vacancy.name, "Не указано")
        self.assertEqual(empty_vacancy.url, "Не указано")
        self.assertEqual(empty_vacancy.salary, "Зарплата не указана")
        self.assertEqual(empty_vacancy.description, "Описание отсутствует")

    def test_format_salary_with_dict(self):
        salary_dict = {
            "from": 100000,
            "to": 150000,
            "currency": "RUB"
        }
        vacancy = Vacancy("Test", "url", salary_dict, "desc")
        self.assertEqual(vacancy.salary, "100000 - 150000 RUB")

    def test_format_salary_with_only_from(self):
        salary_dict = {"from": 100000}
        vacancy = Vacancy("Test", "url", salary_dict, "desc")
        self.assertEqual(vacancy.salary, "100000 RUB")

    def test_format_salary_with_only_to(self):
        salary_dict = {"to": 150000}
        vacancy = Vacancy("Test", "url", salary_dict, "desc")
        self.assertEqual(vacancy.salary, "до 150000 RUB")

    def test_format_salary_with_empty_dict(self):
        salary_dict = {}
        vacancy = Vacancy("Test", "url", salary_dict, "desc")
        self.assertEqual(vacancy.salary, "Зарплата не указана")

    def test_format_salary_with_string(self):
        # Тест с простой строкой зарплаты (целое число)
        vacancy1 = Vacancy("Test", "url", "200000 RUB", "desc")
        self.assertEqual(vacancy1.salary, "200000 RUB")

        # Тест с дробным числом
        vacancy2 = Vacancy("Test", "url", "200000.50 RUB", "desc")
        self.assertEqual(vacancy2.salary, "200000.5 RUB")

        # Тест с некорректной строкой
        vacancy3 = Vacancy("Test", "url", "некорректная строка", "desc")
        self.assertEqual(vacancy3.salary, "Зарплата не указана")

        # Тест с числом без валюты
        vacancy4 = Vacancy("Test", "url", "200000", "desc")
        self.assertEqual(vacancy4.salary, "200000 RUB")

        # Тест с пробелами
        vacancy5 = Vacancy("Test", "url", " 200 000 RUB ", "desc")
        self.assertEqual(vacancy5.salary, "200000 RUB")

        # Тест с диапазоном зарплат (целые числа)
        vacancy6 = Vacancy("Test", "url", {"from": 150000, "to": 250000, "currency": "RUB"}, "desc")
        self.assertEqual(vacancy6.salary, "150000 - 250000 RUB")

        # Тест с диапазоном зарплат (дробные числа)
        vacancy7 = Vacancy("Test", "url", {"from": 150000.5, "to": 250000.75, "currency": "RUB"}, "desc")
        self.assertEqual(vacancy7.salary, "150000.5 - 250000.75 RUB")

        # Тест с только верхней границей
        vacancy8 = Vacancy("Test", "url", {"to": 250000, "currency": "RUB"}, "desc")
        self.assertEqual(vacancy8.salary, "до 250000 RUB")

        # Тест с только нижней границей
        vacancy9 = Vacancy("Test", "url", {"from": 150000, "currency": "RUB"}, "desc")
        self.assertEqual(vacancy9.salary, "150000 RUB")

        # Тест с пустой строкой
        vacancy10 = Vacancy("Test", "url", "", "desc")
        self.assertEqual(vacancy10.salary, "Зарплата не указана")

        # Тест с нулем
        vacancy11 = Vacancy("Test", "url", "0 RUB", "desc")
        self.assertEqual(vacancy11.salary, "0 RUB")

        # Тест с отрицательным числом
        vacancy12 = Vacancy("Test", "url", "-200000 RUB", "desc")
        self.assertEqual(vacancy12.salary, "-200000 RUB")

        # Тест с разными пробелами и форматами
        vacancy13 = Vacancy("Test", "url", " 200 000 RUB ", "desc")
        self.assertEqual(vacancy13.salary, "200000 RUB")

        # Тест с другой валютой
        vacancy15 = Vacancy("Test", "url", {"from": 1500, "to": 2500, "currency": "USD"}, "desc")
        self.assertEqual(vacancy15.salary, "1500 - 2500 USD")



    def test_to_dict(self):
        expected_dict = {
            "name": "Python Developer",
            "url": "https://example.com",
            "salary": "100000",
            "description": "Опытный разработчик"
        }
        self.assertEqual(self.vacancy.to_dict(), expected_dict)

    def test_equality(self):
        # Проверяем равенство при одинаковой зарплате
        vacancy1 = Vacancy("Test1", "url1", "100000", "desc1")
        vacancy2 = Vacancy("Test2", "url2", "100000", "desc2")
        self.assertTrue(vacancy1 == vacancy2)

        # Проверяем неравенство при разной зарплате
        vacancy3 = Vacancy("Test3", "url3", "150000", "desc3")
        self.assertFalse(vacancy1 == vacancy3)

    def test_less_than(self):
        vacancy1 = Vacancy("Test1", "url1", "100000", "desc1")
        vacancy2 = Vacancy("Test2", "url2", "150000", "desc2")
        vacancy3 = Vacancy("Test3", "url3", "50000", "desc3")

        # Базовое сравнение
        self.assertTrue(vacancy1 < vacancy2)  # 100000 < 150000
        self.assertFalse(vacancy2 < vacancy1)  # 150000 не меньше 100000

        # Сравнение с меньшей зарплатой
        self.assertTrue(vacancy3 < vacancy1)  # 50000 < 100000
        self.assertFalse(vacancy1 < vacancy3)  # 100000 не меньше 50000

        # Сравнение с одинаковыми зарплатами
        vacancy4 = Vacancy("Test4", "url4", "100000", "desc4")
        self.assertFalse(vacancy1 < vacancy4)  # 100000 не меньше 100000
        self.assertFalse(vacancy4 < vacancy1)  # 100000 не меньше 100000

        # Сравнение со строкой "Зарплата не указана"
        vacancy5 = Vacancy("Test5", "url5", "", "desc5")
        self.assertFalse(vacancy1 < vacancy5)  # 100000 не меньше "Зарплата не указана"
        self.assertTrue(vacancy5 < vacancy1)  # "Зарплата не указана" меньше 100000

        # Дополнительные проверки
        vacancy6 = Vacancy("Test6", "url6", "", "desc6")
        self.assertFalse(vacancy5 < vacancy6)  # Обе без зарплаты


    # Предположим, что этот код находится в том же файле, что и BaseStorage
class TestBaseStorage(unittest.TestCase):

    class MockStorage(BaseStorage):
        def __init__(self):
            self.data = []
            self.deleted_ids = []

        # def add_vacancy(self, vacancy: Dict):
        #     self.data.append(vacancy)
        def add_vacancy(self, vacancy: Dict):
            # Проверяем уникальность ID перед добавлением
            if any(v['id'] == vacancy['id'] for v in self.data):
                raise ValueError("Вакансия с таким ID уже существует")
            self.data.append(vacancy)

        def get_vacancies(self) -> List[Dict]:
            return self.data

        # def delete_vacancy(self, vacancy_id: int):
        #     self.deleted_ids.append(vacancy_id)
        def delete_vacancy(self, vacancy_id: int):
            # Находим вакансию по ID и удаляем её
            for i, vacancy in enumerate(self.data):
                if vacancy['id'] == vacancy_id:
                    del self.data[i]
                    self.deleted_ids.append(vacancy_id)
                    return
            # Если вакансия не найдена, добавляем ID в список удаленных
            self.deleted_ids.append(vacancy_id)

    def setUp(self):
        # Создаем экземпляр тестового хранилища
        self.storage = self.MockStorage()

    def test_add_vacancy(self):
        vacancy = {
            "id": 1,
            "name": "Тестировщик",
            "url": "http://test.com",
            "salary": "100000",
            "description": "Тестовая вакансия"
        }

        # Добавляем вакансию
        self.storage.add_vacancy(vacancy)

        # Проверяем, что вакансия добавлена
        self.assertEqual(len(self.storage.get_vacancies()), 1)
        # self.assertEqual(self.storage.get_vacancies()[0], vacancy)

        # Удаляем вакансию
        self.storage.delete_vacancy(1)

        # Проверяем, что вакансия удалена
        self.assertEqual(len(self.storage.get_vacancies()), 0)
        self.assertEqual(self.storage.deleted_ids, [1])

    def test_get_vacancies_empty(self):
        # Проверяем пустой список
        self.assertEqual(self.storage.get_vacancies(), [])

    def test_get_vacancies_multiple(self):
        # Добавляем несколько вакансий
        vacancies = [
            {
                "id": 1,
                "name": "Тестировщик 1",
                "url": "http://test1.com",
                "salary": "100000",
                "description": "Описание 1"
            },
            {
                "id": 2,
                "name": "Тестировщик 2",
                "url": "http://test2.com",
                "salary": "120000",
                "description": "Описание 2"
            }
        ]

        for vac in vacancies:
            self.storage.add_vacancy(vac)

        # Проверяем получение всех вакансий
        self.assertEqual(self.storage.get_vacancies(), vacancies)

    def test_delete_vacancy(self):
        vacancy = {
            "id": 1,
            "name": "Тестировщик",
            "url": "http://test.com",
            "salary": "100000",
            "description": "Тестовая вакансия"
        }

        # Добавляем вакансию
        self.storage.add_vacancy(vacancy)

        # Проверяем, что вакансия добавлена
        self.assertEqual(len(self.storage.get_vacancies()), 1)

        # Удаляем вакансию
        self.storage.delete_vacancy(1)

        # Проверяем, что вакансия удалена
        self.assertEqual(len(self.storage.get_vacancies()), 0)
        self.assertEqual(self.storage.deleted_ids, [1])

    def test_delete_nonexistent_vacancy(self):
        # Пытаемся удалить несуществующую вакансию
        self.storage.delete_vacancy(999)

        # Проверяем, что список не изменился
        self.assertEqual(len(self.storage.get_vacancies()), 0)
        self.assertEqual(self.storage.deleted_ids, [999])

    def test_delete_multiple_vacancies(self):
        # Добавляем несколько вакансий
        vacancies = [
            {
                "id": 1,
                "name": "Тестировщик 1",
                "url": "http://test1.com",
                "salary": "100000",
                "description": "Описание 1"
            },
            {
                "id": 2,
                "name": "Тестировщик 2",
                "url": "http://test2.com",
                "salary": "120000",
                "description": "Описание 2"
            }
        ]

        for vac in vacancies:
            self.storage.add_vacancy(vac)

        # Удаляем одну вакансию
        self.storage.delete_vacancy(1)

        # Проверяем, что осталась только одна вакансия
        self.assertEqual(len(self.storage.get_vacancies()), 1)
        self.assertEqual(self.storage.get_vacancies()[0]['id'], 2)
        self.assertEqual(self.storage.deleted_ids, [1])

    def test_delete_nonexistent_vacancy(self):
        # Пытаемся удалить несуществующую вакансию
        self.storage.delete_vacancy(999)

        # Проверяем, что список удаленных ID содержит ID
        self.assertEqual(self.storage.deleted_ids, [999])

    def test_abstract_methods(self):
        # Проверяем, что нельзя создать экземпляр абстрактного класса
        with self.assertRaises(TypeError):
            BaseStorage()