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


def predict_rub_salary_hh(programing_languages):
    salary = []
    for page in count(0):
        param = {"text": f"Программист {programing_languages}",
                 "area": "1",
                 "page": f"{page}",
                 "only_with_salary": "true"}
        response = requests.get("https://api.hh.ru/vacancies/", params=param).json()

        if not response["found"]:
            return {"vacancies_found": 0, "vacancies_processed": 0,
                    "average_salary": 0}

        if page == response["pages"]:
            break

        for vacancy in response["items"]:
            if vacancy["salary"]["currency"] == "RUR":
                salary_from = vacancy["salary"]["from"]
                salary_to = vacancy["salary"]["to"]
                salary.append(predict_salary(salary_from, salary_to))

    data_filtering = [i for i in salary if i is not None]
    average_salary = int(sum(data_filtering) / len(data_filtering))
    return {"vacancies_found": response["found"], "vacancies_processed": len(data_filtering),
            "average_salary": average_salary}


def predict_rub_salary_sj(programing_languages, x_api_app_id, authorization):
    header = {
        "X-Api-App-Id": x_api_app_id,
        "Authorization": authorization,
    }
    salary = []
    for page in count(0):
        parametrs = {"page": f"{page}",
                     "catalogues": "48",
                     "t": "4",
                     "keyword": f"Программист {programing_languages}",
                     "more": "true", }
        response = requests.get("https://api.superjob.ru/2.0/vacancies/", headers=header, params=parametrs).json()
        if not response["total"]:
            return {"vacancies_found": 0, "vacancies_processed": 0,
                    "average_salary": 0}
        for vacancy in response["objects"]:
            if vacancy["currency"] == "rub":
                salary_from = vacancy["payment_from"]
                salary_to = vacancy["payment_to"]
                salary.append(predict_salary(salary_from, salary_to))
        if not response["more"]:
            break
    data_filtering = [i for i in salary if i is not None]
    average_salary = int(sum(data_filtering) / len(data_filtering))
    return {"vacancies_found": response["total"], "vacancies_processed": len(data_filtering),
            "average_salary": average_salary}


def show_table(superjob_stats, headhunter_stats):
    superjob_table = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"],
        [superjob_stats[0][0], superjob_stats[0][1], superjob_stats[0][2], superjob_stats[0][3]],
        [superjob_stats[1][0], superjob_stats[1][1], superjob_stats[1][2], superjob_stats[1][3]],
        [superjob_stats[2][0], superjob_stats[2][1], superjob_stats[2][2], superjob_stats[2][3]],
        [superjob_stats[3][0], superjob_stats[3][1], superjob_stats[3][2], superjob_stats[3][3]],
        [superjob_stats[4][0], superjob_stats[4][1], superjob_stats[4][2], superjob_stats[4][3]],
        [superjob_stats[5][0], superjob_stats[5][1], superjob_stats[5][2], superjob_stats[5][3]],
        [superjob_stats[6][0], superjob_stats[6][1], superjob_stats[6][2], superjob_stats[6][3]],
        [superjob_stats[7][0], superjob_stats[7][1], superjob_stats[7][2], superjob_stats[7][3]],
        [superjob_stats[8][0], superjob_stats[8][1], superjob_stats[8][2], superjob_stats[8][3]],
        [superjob_stats[9][0], superjob_stats[9][1], superjob_stats[9][2], superjob_stats[9][3]],

    ]
    headhunter_table = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"],
        [headhunter_stats[0][0], headhunter_stats[0][1], headhunter_stats[0][2], headhunter_stats[0][3]],
        [headhunter_stats[1][0], headhunter_stats[1][1], headhunter_stats[1][2], headhunter_stats[1][3]],
        [headhunter_stats[2][0], headhunter_stats[2][1], headhunter_stats[2][2], headhunter_stats[2][3]],
        [headhunter_stats[3][0], headhunter_stats[3][1], headhunter_stats[3][2], headhunter_stats[3][3]],
        [headhunter_stats[4][0], headhunter_stats[4][1], headhunter_stats[4][2], headhunter_stats[4][3]],
        [headhunter_stats[5][0], headhunter_stats[5][1], headhunter_stats[5][2], headhunter_stats[5][3]],
        [headhunter_stats[6][0], headhunter_stats[6][1], headhunter_stats[6][2], headhunter_stats[6][3]],
        [headhunter_stats[7][0], headhunter_stats[7][1], headhunter_stats[7][2], headhunter_stats[7][3]],
        [headhunter_stats[8][0], headhunter_stats[8][1], headhunter_stats[8][2], headhunter_stats[8][3]],
        [headhunter_stats[9][0], headhunter_stats[9][1], headhunter_stats[9][2], headhunter_stats[9][3]],

    ]

    superjob_moscow_title = 'SuperJob Moscow'
    headhunter_moscow_title = 'HeadHunter Moscow'
    table_instance_superjob = AsciiTable(superjob_table, superjob_moscow_title)
    table_instance_headhunter = AsciiTable(headhunter_table, headhunter_moscow_title)
    print(table_instance_headhunter.table)
    print()
    print(table_instance_superjob.table)


def get_table(table_stats):
    table = []
    for lang, stats, in table_stats.items():
        table.append([lang, stats["vacancies_found"], stats["vacancies_processed"], stats["average_salary"]])
    return table


def main():
    load_dotenv()
    x_api_app_id = os.getenv("X_API_APP_ID")
    authorization = os.getenv("AUTHORIZATION")

    programing_languages = ["GO", "JavaScript",
                            "Java", "Python",
                            "Ruby", "PHP",
                            "C++", "C#",
                            "C", "TypeScript",
                            ]

    sj_language_statistics = {}
    hh_language_statistics = {}
    for language in programing_languages:
        hh_language_statistics[language] = predict_rub_salary_hh(language)
        sj_language_statistics[language] = predict_rub_salary_sj(language, x_api_app_id, authorization)

    sj_table_stats = get_table(sj_language_statistics)
    hh_table_stats = get_table(hh_language_statistics)
    show_table(sj_table_stats, hh_table_stats)


if __name__ == "__main__":
    main()
