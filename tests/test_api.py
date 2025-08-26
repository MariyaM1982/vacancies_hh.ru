import unittest
from unittest.mock import MagicMock, patch


from api.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self):
        self.api = HeadHunterAPI()

    @patch("requests.get")
    def test_connect(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        self.api._connect()
        mock_get.assert_called_once_with(self.api._base_url)

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Тестировщик",
                    "url": "http://test.com",
                    "salary": {"from": 100000},
                    "description": "Тестовый описание",
                }
            ]
        }
        mock_get.return_value = mock_response

        result = self.api.get_vacancies("Python")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Тестировщик")

    @patch("requests.get")
    def test_get_vacancies_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.get_vacancies("Python")
        self.assertEqual(result, [])
