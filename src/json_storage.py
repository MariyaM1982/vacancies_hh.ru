import json
import os
from typing import Dict, List, Optional


class JSONStorage:
    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename
        # Проверяем существование файла при инициализации
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_vacancy(self, vacancy: Dict) -> None:
        try:
            # Читаем существующие данные
            with open(self._filename, "r+", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

                # Проверяем дубликаты по URL
                if not any(v["url"] == vacancy["url"] for v in data):
                    data.append(vacancy)

                # Перезаписываем файл
                file.seek(0)
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.truncate()
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def get_vacancies(self) -> List[Dict]:
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении данных: {e}")
            return []

    def delete_vacancy(self, url: str) -> bool:
        try:
            with open(self._filename, "r+", encoding="utf-8") as file:
                data = json.load(file)
                original_length = len(data)

                # Фильтруем вакансии
                data = [v for v in data if v["url"] != url]

                # Сохраняем изменения только если что-то изменилось
                if len(data) < original_length:
                    file.seek(0)
                    json.dump(data, file, ensure_ascii=False, indent=4)
                    file.truncate()
                    return True
                return False
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
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
