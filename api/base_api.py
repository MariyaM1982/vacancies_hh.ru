from abc import ABC, abstractmethod


class BaseAPI(ABC):
    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def get_vacancies(self, query: str) -> list:
        pass
