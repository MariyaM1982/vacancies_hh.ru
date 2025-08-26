from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: dict):
        pass

    @abstractmethod
    def get_vacancies(self) -> list:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: int):
        pass
