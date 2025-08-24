import json
from typing import Dict, List, Optional

from src.base_storage import BaseStorage


class JSONStorage(BaseStorage):
    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename

    def add_vacancy(self, vacancy: Dict) -> None:
        """
        Добавляет вакансию в файл
        :param vacancy: словарь с данными вакансии
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        # Проверяем уникальность вакансии по URL
        if not any(v["url"] == vacancy["url"] for v in data):
            data.append(vacancy)
            with open(self._filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

    def get_vacancies(self) -> List[Dict]:
        """
        Получает все вакансии из файла
        :return: список словарей с вакансиями
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def delete_vacancy(self, url: str) -> bool:
        """
        Удаляет вакансию по URL
        :param url: URL вакансии для удаления
        :return: True если вакансия была удалена, False если не найдена
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return False

        updated_data = [v for v in data if v["url"] != url]
        if len(updated_data) < len(data):
            with open(self._filename, "w", encoding="utf-8") as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)
            return True
        return False

    def filter_vacancies(
        self,
        keyword: Optional[str] = None,
        min_salary: Optional[int] = None,
        max_salary: Optional[int] = None,
    ) -> List[Dict]:
        """
        Фильтрует вакансии по заданным параметрам
        :param keyword: ключевое слово для поиска в описании
        :param min_salary: минимальная зарплата
        :param max_salary: максимальная зарплата
        :return: отфильтрованный список вакансий
        """
        vacancies = self.get_vacancies()

        if keyword:
            vacancies = [
                v for v in vacancies if keyword.lower() in v["description"].lower()
            ]

        if min_salary is not None:
            vacancies = [v for v in vacancies if self._parse_salary(v) >= min_salary]

        if max_salary is not None:
            vacancies = [v for v in vacancies if self._parse_salary(v) <= max_salary]

        return vacancies

    def _parse_salary(self, vacancy: Dict) -> int:
        """
        Парсит зарплату из строки в число
        :param vacancy: словарь с данными вакансии
        :return: зарплата в виде числа или 0 если не удалось распарсить
        """
        salary_str = vacancy.get("salary", "")
        try:
            # Упрощенный парсинг зарплаты
            # В реальной реализации нужно учитывать разные форматы зарплат
            return int("".join(filter(str.isdigit, salary_str)))
        except ValueError:
            return 0
