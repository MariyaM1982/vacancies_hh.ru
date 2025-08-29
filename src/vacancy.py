class Vacancy:
    __slots__ = ("name", "url", "salary", "description")

    def __init__(self, name: str, url: str, salary: str, description: str):
        self._salary = None
        self.name = name or "Не указано"
        self.url = url or "Не указано"
        self.salary = self._format_salary(salary)
        self.description = description or "Описание отсутствует"

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        # Проверяем наличие зарплат
        if self._salary is None and other._salary is None:
            return False  # Обе зарплаты не указаны
        if self._salary is None:
            return False  # Текущая вакансия без зарплаты
        if other._salary is None:
            return True  # Другая вакансия без зарплаты

        return self._salary < other._salary

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }

    def _format_salary(self, salary: str) -> str:
        try:
            if isinstance(salary, dict):
                salary_from = salary.get("from", None)
                salary_to = salary.get("to", None)
                currency = salary.get("currency", "RUB")

                if salary_from and salary_to:
                    return f"{salary_from} - {salary_to} {currency}"
                elif salary_from:
                    return f"{salary_from} {currency}"
                elif salary_to:
                    return f"до {salary_to} {currency}"  # Изменили формат
                else:
                    return "Зарплата не указана"

            return salary if salary else "Зарплата не указана"
        except Exception:
            return "Зарплата не указана"

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }
