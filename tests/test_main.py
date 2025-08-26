import json
import os
import unittest
from unittest.mock import patch
from main import main
from src.vacancy import Vacancy


class TestMainFunctionality(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.test_vacancy_data = {
            "name": "Тестировщик",
            "url": "http://test.com",
            "salary": "100000",
            "description": "Тестовый описание",
        }
        self.test_vacancy = Vacancy(**self.test_vacancy_data)

        # Создаем тестовый файл
        with open("test_vacancies.json", "w") as f:
            json.dump([self.test_vacancy_data], f)

    def tearDown(self):
        # Удаляем тестовый файл
        if os.path.exists("test_vacancies.json"):
            os.remove("test_vacancies.json")

    def test_exit_program(self):
        # Имитируем ввод пользователя
        with patch("builtins.input", return_value="4"):
            with self.assertRaises(SystemExit):
                main()
