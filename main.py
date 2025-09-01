from api.hh_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_storage import JSONStorage
from src.helpers import print_vacancies, sort_vacancies_by_salary
import sys


def main():
    print("Приветствуем в системе поиска вакансий!")

    # Инициализация компонентов
    api = HeadHunterAPI()
    storage = JSONStorage()

    while True:
        print("\nВыберите действие:")
        print("1. Поиск новых вакансий")
        print("2. Показать топ вакансий по зарплате")
        print("3. Поиск по ключевым словам")
        print("4. Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            query = input("Введите поисковый запрос: ")
            try:
                vacancies_data = api.get_vacancies(query)

                # Проверяем, что получили список
                if not isinstance(vacancies_data, list):
                    print("Ошибка получения данных от API")
                    continue

                # Фильтруем только валидные вакансии
                vacancies = [
                    Vacancy(
                        name=data.get('name', 'Не указано'),
                        url=data.get('alternate_url', 'Не указано'),
                        salary=data.get('salary', 'Зарплата не указана'),  # Передаем словарь зарплаты
                        description=data.get('snippet', {}).get('responsibility', 'Описание отсутствует')
                    )
                    for data in vacancies_data if isinstance(data, dict)
                ]

                for vacancy in vacancies:
                    storage.add_vacancy(vacancy.to_dict())
                print(f"Найдено и сохранено {len(vacancies)} вакансий")

            except Exception as e:
                print(f"Ошибка при получении данных: {e}")

        elif choice == '2':
            try:
                top_n = int(input("Введите количество вакансий для отображения в топе: "))
                vacancies = storage.get_vacancies()

                # Проверяем, что данные корректны
                if not isinstance(vacancies, list):
                    print("Ошибка: некорректные данные в хранилище")
                    continue

                # Преобразуем словари в объекты Vacancy
                vacancies = [Vacancy(**v) for v in vacancies if isinstance(v, dict)]

                # Сортируем только если есть вакансии
                if vacancies:
                    sorted_vacancies = sort_vacancies_by_salary(vacancies)
                    top_vacancies = sorted_vacancies[:top_n]
                    print(f"\nТоп-{top_n} вакансий по зарплате:")
                    print_vacancies(top_vacancies)

                else:
                    print("Вакансии не найдены")

            except ValueError:
                print("Ошибка: введите число")

            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '3':
            try:
                keyword = input("Введите ключевое слово для поиска: ")
                vacancies = storage.filter_vacancies(keyword=keyword)
                if vacancies:
                    print(f"\nНайдено {len(vacancies)} вакансий по запросу '{keyword}':")
                    print_vacancies([Vacancy(**v) for v in vacancies])
                else:
                    print("Вакансии не найдены")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '4':
            print("До свидания!")
            sys.exit(0)

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()