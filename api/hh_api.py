import requests

from api.base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"
        self._connect()

    def _connect(self):
        response = requests.get(self._base_url)
        if response.status_code != 200:
            raise ConnectionError("Не удалось подключиться к API")

    def get_vacancies(self, query: str) -> list:
        params = {"text": query, "per_page": 100}
        response = requests.get(self._base_url, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        return []
