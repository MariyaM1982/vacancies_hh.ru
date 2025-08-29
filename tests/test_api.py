import unittest
from unittest.mock import MagicMock, patch
import logging

import requests

from api.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self):
        self.api = HeadHunterAPI()
        # Настроим логирование для тестирования
        logging.basicConfig(level=logging.ERROR)

    @patch("requests.get")
    def test_get_vacancies(self, mock_get):
        # Создаём мок ответа
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Тестовая вакансия",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
                    "snippet": {"responsibility": "Описание обязанностей"},
                }
            ]
        }

        mock_get.return_value = mock_response

        # Вызываем метод с тестовым запросом
        result = self.api.get_vacancies("python")

        # Проверяем, что запрос был сделан правильно
        mock_get.assert_called_once_with(
            self.api.base_url,
            params={"text": "python", "per_page": 100, "area": 1},
            headers=self.api.headers,
        )

        # Проверяем результат
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Тестовая вакансия")

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        # Успешный случай
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Тестовая вакансия",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
                    "snippet": {"responsibility": "Описание обязанностей"},
                }
            ]
        }
        mock_get.return_value = mock_response

        result = self.api.get_vacancies("python")
        self.assertEqual(len(result), 1)

    @patch("requests.get")
    def test_get_vacancies_error(self, mock_get):
        # Случай с ошибкой статуса
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.get_vacancies("python")
        self.assertEqual(result, [])  # Проверяем пустой список

    @patch("requests.get")
    def test_get_vacancies_invalid_response(self, mock_get):
        # Случай с некорректным форматом ответа
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = "Неверный формат"
        mock_get.return_value = mock_response

        result = self.api.get_vacancies("python")
        self.assertEqual(result, [])  # Проверяем пустой список

    @patch("requests.get")
    def test_get_vacancies_no_items(self, mock_get):
        # Случай без вакансий в ответе
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = self.api.get_vacancies("python")
        self.assertEqual(result, [])  # Проверяем пустой список

    @patch("requests.get")
    def test_get_vacancies_network_error(self, mock_get):
        # Случай с сетевой ошибкой
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = self.api.get_vacancies("python")
        self.assertEqual(result, [])  # Проверяем пустой список
