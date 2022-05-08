import os
from itertools import count

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to not in {None, 0}:
        return int((salary_from + salary_to) / 2)
    if salary_from not in {None, 0}:
        return int(salary_from * 0.8)
    if salary_to not in {None, 0}:
        return int(salary_to * 1.2)
    else:
        return None


def head_hunter(programing_languages):
    hh_language_statistics = {}
    for languages in programing_languages:
        salary = []
        for page in count(0):
            param = {"text": f"Программист {languages}",
                     "area": "1",
                     "page": f"{page}",
                     "only_with_salary": "true"}
            response = requests.get("https://api.hh.ru/vacancies/", params=param).json()
            if page == response["pages"]:
                break
            for vacancy in response["items"]:
                if vacancy["salary"]["currency"] == "RUR":
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]
                    salary.append(predict_salary(salary_from, salary_to))

        salary = [i for i in salary if i is not None]
        average_salary = int(sum(salary) / len(salary))
        hh_language_statistics.update({languages: {"vacancies_found": response["found"],
                                                   "vacancies_processed": len(salary),
                                                   "average_salary": average_salary}})
    return hh_language_statistics


def super_job(programing_languages):
    sj_language_statistics = {}
    header = {
        "X-Api-App-Id": X_API_APP_ID,
        "Authorization": AUTHORIZATION,
    }
    for languages in programing_languages:
        salary = []
        for page in count(0):
            parametrs = {"page": f"{page}",
                         "catalogues": "48",
                         "t": "4",
                         "keyword": f"Программист {languages}",
                         "more": "true", }
            response = requests.get("https://api.superjob.ru/2.0/vacancies/", headers=header, params=parametrs).json()

            for vacancy in response["objects"]:
                if vacancy["currency"] == "rub":
                    salary_from = vacancy["payment_from"]
                    salary_to = vacancy["payment_to"]
                    salary.append(predict_salary(salary_from, salary_to))
            if not response["more"]:
                break
        salary = [i for i in salary if i is not None]
        average_salary = int(sum(salary) / len(salary))
        sj_language_statistics.update({languages: {"vacancies_found": response["total"],
                                                   "vacancies_processed": len(salary),
                                                   "average_salary": average_salary}})
    return sj_language_statistics


def table_show(superjob_data, headhunter_data):
    superjob_table = (
        ('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'),
        ("GO", superjob_data["GO"]["vacancies_found"], superjob_data["GO"]["vacancies_processed"],
         superjob_data["GO"]["average_salary"]),
        ("JavaScript", superjob_data["JavaScript"]["vacancies_found"],
         superjob_data["JavaScript"]["vacancies_processed"],
         superjob_data["JavaScript"]["average_salary"]),
        ("Java", superjob_data["Java"]["vacancies_found"],
         superjob_data["Java"]["vacancies_processed"], superjob_data["Java"]["average_salary"]),
        ("Python", superjob_data["Python"]["vacancies_found"],
         superjob_data["Python"]["vacancies_processed"], superjob_data["Python"]["average_salary"]),
        ("Ruby", superjob_data["Ruby"]["vacancies_found"],
         superjob_data["Ruby"]["vacancies_processed"], superjob_data["Ruby"]["average_salary"]),
        ("PHP", superjob_data["PHP"]["vacancies_found"], superjob_data["PHP"]["vacancies_processed"],
         superjob_data["PHP"]["average_salary"]),
        ("C++", superjob_data["C++"]["vacancies_found"], superjob_data["C++"]["vacancies_processed"],
         superjob_data["C++"]["average_salary"]),
        ("C#", superjob_data["C#"]["vacancies_found"], superjob_data["C#"]["vacancies_processed"],
         superjob_data["C#"]["average_salary"]),
        ("C", superjob_data["C"]["vacancies_found"], superjob_data["C"]["vacancies_processed"],
         superjob_data["C"]["average_salary"]),
        ("TypeScript", superjob_data["TypeScript"]["vacancies_found"],
         superjob_data["TypeScript"]["vacancies_processed"],
         superjob_data["TypeScript"]["average_salary"]),
    )

    headhunter_table = (
        ('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'),
        ("GO", headhunter_data["GO"]["vacancies_found"], headhunter_data["GO"]["vacancies_processed"],
         headhunter_data["GO"]["average_salary"]),
        ("JavaScript", headhunter_data["JavaScript"]["vacancies_found"],
         headhunter_data["JavaScript"]["vacancies_processed"],
         headhunter_data["JavaScript"]["average_salary"]),
        ("Java", headhunter_data["Java"]["vacancies_found"],
         headhunter_data["Java"]["vacancies_processed"], headhunter_data["Java"]["average_salary"]),
        ("Python", headhunter_data["Python"]["vacancies_found"],
         headhunter_data["Python"]["vacancies_processed"], headhunter_data["Python"]["average_salary"]),
        ("Ruby", headhunter_data["Ruby"]["vacancies_found"],
         headhunter_data["Ruby"]["vacancies_processed"], headhunter_data["Ruby"]["average_salary"]),
        ("PHP", headhunter_data["PHP"]["vacancies_found"], headhunter_data["PHP"]["vacancies_processed"],
         headhunter_data["PHP"]["average_salary"]),
        ("C++", headhunter_data["C++"]["vacancies_found"], headhunter_data["C++"]["vacancies_processed"],
         headhunter_data["C++"]["average_salary"]),
        ("C#", headhunter_data["C#"]["vacancies_found"], headhunter_data["C#"]["vacancies_processed"],
         headhunter_data["C#"]["average_salary"]),
        ("C", headhunter_data["C"]["vacancies_found"], headhunter_data["C"]["vacancies_processed"],
         headhunter_data["C"]["average_salary"]),
        ("TypeScript", headhunter_data["TypeScript"]["vacancies_found"],
         headhunter_data["TypeScript"]["vacancies_processed"],
         headhunter_data["TypeScript"]["average_salary"]),
    )

    superjob_moscow_title = 'SuperJob Moscow'
    headhunter_moscow_title = 'HeadHunter Moscow'
    table_instance_superjob = AsciiTable(superjob_table, superjob_moscow_title)
    table_instance_headhunter = AsciiTable(headhunter_table, headhunter_moscow_title)
    table_instance_superjob.justify_columns[2] = 'right'
    table_instance_headhunter.justify_columns[2] = 'right'
    print(table_instance_headhunter.table)
    print()
    print(table_instance_superjob.table)


def main():
    programing_languages = ["GO", "JavaScript",
                            "Java", "Python",
                            "Ruby", "PHP",
                            "C++", "C#",
                            "C", "TypeScript",
                            ]
    superjob_data = super_job(programing_languages)

    headhunter_data = head_hunter(programing_languages)
    table_show(superjob_data, headhunter_data)


if __name__ == "__main__":
    load_dotenv()
    X_API_APP_ID = os.getenv("X_API_APP_ID")
    AUTHORIZATION = os.getenv("AUTHORIZATION")
    main()
