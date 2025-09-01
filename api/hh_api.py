import requests
from typing import List, Dict
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HeadHunterAPI:
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"  # Базовый URL API
        self.headers = {
            "User-Agent": "Mozilla/5.0"  # Добавляем заголовок для корректной работы
        }

    def get_vacancies(self, query: str) -> List[Dict]:
        try:
            response = requests.get(
                self.base_url,
                params={
                    "text": query,
                    "per_page": 100,
                    "area": 1,  # Москва и МО (можно убрать, если не нужно)
                },
                headers=self.headers,
            )

            response.raise_for_status()  # Проверяем статус ответа

            data = response.json()

            # Проверяем структуру ответа
            if isinstance(data, dict) and "items" in data:
                return data["items"]

            logger.error("Неверный формат ответа от API")
            return []

        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            return []

        except Exception as e:
            logger.error(f"Произошла ошибка: {e}")
            return []
