import os
from itertools import count

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    if salary_from:
        return int(salary_from * 0.8)
    if salary_to:
        return int(salary_to * 1.2)


def predict_rub_salary_hh(programming_language):
    url = "https://api.hh.ru/vacancies/"
    salaries = []
    for page in count(0):
        param = {
            "text": f"Программист {programming_language}",
            "area": "1",
            "page": f"{page}",
            "only_with_salary": "true"
        }
        response = requests.get(url, params=param)
        response.raise_for_status()
        decoded_response = response.json()

        if page == decoded_response["pages"]:
            break

        for vacancy in decoded_response["items"]:
            if vacancy["salary"]["currency"] == "RUR":
                salary_from = vacancy["salary"]["from"]
                salary_to = vacancy["salary"]["to"]
                salary = predict_salary(salary_from, salary_to)
                if not salary:
                    continue
                salaries.append(salary)

    average_salary = int(sum(salaries) / len(salaries)) if salaries else 0
    return {
        "vacancies_found": decoded_response["found"],
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }


def predict_rub_salary_sj(programming_language, x_api_app_id, authorization):
    url = "https://api.superjob.ru/2.0/vacancies/"
    header = {
        "X-Api-App-Id": x_api_app_id,
        "Authorization": authorization,
    }
    salaries = []
    for page in count(0):
        param = {
            "page": f"{page}",
            "catalogues": "48",
            "t": "4",
            "keyword": f"Программист {programming_language}",
            "more": "true"
        }
        response = requests.get(url, headers=header, params=param)
        response.raise_for_status()
        decoded_response = response.json()

        for vacancy in decoded_response["objects"]:
            if vacancy["currency"] == "rub":
                salary_from = vacancy["payment_from"]
                salary_to = vacancy["payment_to"]
                salary = predict_salary(salary_from, salary_to)
                if not salary:
                    continue
                salaries.append(salary)
        if not decoded_response["more"]:
            break

    average_salary = int(sum(salaries) / len(salaries)) if salaries else 0
    return {
        "vacancies_found": decoded_response["total"],
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }


def get_table(table_stats):
    table = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]
    for lang, stats, in table_stats.items():
        table.append(
            [
                lang,
                stats["vacancies_found"],
                stats["vacancies_processed"],
                stats["average_salary"]
            ]
        )
    return table


def main():
    load_dotenv()
    x_api_app_id = os.getenv("X_API_APP_ID")
    authorization = os.getenv("AUTHORIZATION")

    programing_languages = [
        "GO",
        "JavaScript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "C",
        "TypeScript",

    ]

    sj_language_statistics = {}
    hh_language_statistics = {}
    for language in programing_languages:
        hh_language_statistics[language] = predict_rub_salary_hh(language)
        sj_language_statistics[language] = predict_rub_salary_sj(
            language,
            x_api_app_id,
            authorization
        )
    print(sj_language_statistics)
    sj_table = get_table(sj_language_statistics)
    hh_table = get_table(hh_language_statistics)
    sj_moscow_title = 'SuperJob Moscow'
    headhunter_moscow_title = 'HeadHunter Moscow'
    table_instance_sj = AsciiTable(sj_table, sj_moscow_title)
    table_instance_headhunter = AsciiTable(hh_table, headhunter_moscow_title)
    print(table_instance_headhunter.table)
    print()
    print(table_instance_sj.table)


if __name__ == "__main__":
    main()
