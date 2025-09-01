class Vacancy:
    __slots__ = ("name", "url", "salary", "description", "_salary")

    def __init__(self, name: str, url: str, salary: str, description: str):
        self._salary = None
        self.name = name or "Не указано"
        self.url = url or "Не указано"
        self.salary = self._format_salary(salary)
        self.description = description or "Описание отсутствует"

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        # Извлекаем числовые значения зарплат
        self_numeric_salary = self._extract_numeric_salary()
        other_numeric_salary = other._extract_numeric_salary()

        if self_numeric_salary is None and other_numeric_salary is None:
            return False  # Обе зарплаты не указаны
        if self_numeric_salary is None:
            return False  # Текущая вакансия без зарплаты
        if other_numeric_salary is None:
            return True  # Другая вакансия без зарплаты

        return self_numeric_salary < other_numeric_salary


    def _format_salary(self, salary: str) -> str:
        try:
            if isinstance(salary, dict):
                salary_from = salary.get("from", None)
                salary_to = salary.get("to", None)
                currency = salary.get("currency", "RUB")

                if salary_from and salary_to:
                    self._salary = (salary_from + salary_to) / 2  # Среднее значение
                    # Форматируем числа с учетом дробной части
                    formatted_from = int(salary_from) if isinstance(salary_from,
                                                                    int) or salary_from.is_integer() else salary_from
                    formatted_to = int(salary_to) if isinstance(salary_to,
                                                                int) or salary_to.is_integer() else salary_to
                    return f"{formatted_from} - {formatted_to} {currency}"
                elif salary_from:
                    self._salary = salary_from
                    formatted_value = int(salary_from) if isinstance(salary_from,
                                                                     int) or salary_from.is_integer() else salary_from
                    return f"{formatted_value} {currency}"
                elif salary_to:
                    self._salary = salary_to
                    formatted_value = int(salary_to) if isinstance(salary_to,
                                                                   int) or salary_to.is_integer() else salary_to
                    return f"до {formatted_value} {currency}"
                else:
                    self._salary = None
                    return "Зарплата не указана"
            else:
                # Проверяем, является ли строка числовой с валютой
                if isinstance(salary, str):
                    salary = salary.strip()
                    if 'RUB' in salary:
                        salary_value = salary.replace('RUB', '').replace(' ', '')
                        try:
                            numeric_value = float(salary_value)
                            self._salary = numeric_value
                            # Форматируем число без десятичных знаков, если оно целое
                            formatted_value = int(numeric_value) if numeric_value.is_integer() else numeric_value
                            return f"{formatted_value} RUB"
                        except ValueError:
                            self._salary = None
                            return "Зарплата не указана"
                    else:
                        try:
                            numeric_value = float(salary.replace(' ', ''))
                            self._salary = numeric_value
                            formatted_value = int(numeric_value) if numeric_value.is_integer() else numeric_value
                            return f"{formatted_value} RUB"
                        except ValueError:
                            self._salary = None
                            return "Зарплата не указана"
                else:
                    self._salary = None
                    return "Зарплата не указана"
        except Exception:
            self._salary = None
            return "Зарплата не указана"

    def _extract_numeric_salary(self):
        # Возвращаем числовое значение зарплаты
        return self._salary

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }
