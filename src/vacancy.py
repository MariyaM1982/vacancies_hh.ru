class Vacancy:
    __slots__ = ("name", "url", "salary", "description")

    def __init__(self, name: str, url: str, salary: str, description: str):
        self.name = name
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def _validate_salary(self, salary: str) -> str:
        if not salary:
            return "Зарплата не указана"
        return salary

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }
