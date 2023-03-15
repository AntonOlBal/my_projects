from requests.packages.urllib3.exceptions import InsecureRequestWarning
from jira import JIRA
import requests
import re
import datetime



def main(JIRA_USER, JIRA_PASSWORD, BUILD_VERSION, RELEASE_DATE, DESCRIPTION):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Ignoring the SSL certificate
    jira_option = {
        'server': 'https://jira.psbnk.msk.ru/',
        'verify': False
    }
    jira_connect = JIRA(basic_auth=(JIRA_USER, JIRA_PASSWORD), options=jira_option)

    fact = jira_connect.project("FACT")
    json_project_fact = fact.raw
    # BUILD_VERSION = '22.12.1'

    all_vers_list = []
    error_message = ('=======================================================================================\n'
                     f'ERROR Вы ввели номер версии, который отсутствует в JIRA -> {BUILD_VERSION}\n'
                     'Если хотите создать версию, при старте Pipеline введите переменные RELEASE_DATE и DESCRIPTION\n'
                     'Возможные форматы: xx.xx.xx, xx.x.x, xx.xx.x, xx.x.xx Подсказка: год.месяц.хот_фикс\n'
                     'Если необходимо создать версию отличного от стандартного формата,\n'
                     'необходимо сделать это вручную из Jira\n'
                     '=======================================================================================')

    # Getting  all versions name
    for version in json_project_fact['versions']:
        all_vers_list.append(version['name'])

    # Comparison with all version and released new version
    if BUILD_VERSION not in all_vers_list:
        if re.search(r'^\d{2}\.(0[1-9]|1[012])\.\d{1,2}$', BUILD_VERSION):
            split_name = BUILD_VERSION.split('.')
            date_now = datetime.datetime.now()
            if RELEASE_DATE != '' and DESCRIPTION != '':
                if split_name[0] == date_now.strftime("%y"):
                    jira_connect.create_version(project='FACT', description=f'{DESCRIPTION} (autoCreate)',
                                                name=BUILD_VERSION, releaseDate=RELEASE_DATE)
                    print('=================================================================================\n'
                          f'СОЗДАНА ВЕРСИЯ {BUILD_VERSION} Дата выпуска: {RELEASE_DATE} Описание: {DESCRIPTION}\n'
                          '=================================================================================\n')
                else:
                    print(error_message)
        else:
            print(error_message)


if __name__ == "__main__":
    BUILD_VERSION = input('BUILD_VERSION: ')
    JIRA_USER = input('JIRA_USER: ')
    JIRA_PASSWORD = input('JIRA_PASSWORD: ')
    RELEASE_DATE = input('RELEASE_DATE: ')
    if RELEASE_DATE == "NULL":
        RELEASE_DATE = ""
    DESCRIPTION = input('DESCRIPTION: ')
    if DESCRIPTION == "NULL":
        DESCRIPTION = ""

    main(JIRA_USER, JIRA_PASSWORD, BUILD_VERSION, RELEASE_DATE, DESCRIPTION)

