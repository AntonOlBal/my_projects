import sys
import requests
from jira import JIRA
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging

from select_methods import *
from select_logs import *
from actions import *


def main(JIRA_USER, JIRA_PASSWORD, BUILD_VERSION):
    # Loggining
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # Options
    jira_option = {
        'server': "https://jira/",
        'verify': False
    }
    # Connect to jira
    jira_connect = JIRA(basic_auth=(JIRA_USER, JIRA_PASSWORD), options=jira_option)

    # Issue for test
    # project = FACT AND fixVersion = EMPTY AND issuetype != Ошибка AND status in (Тестирование) AND key in ('FACT-4668', 'FACT-5957')
    all_task = np.array(
        jira_connect.search_issues(
            "project = FACT AND fixVersion = EMPTY AND issuetype != Ошибка AND status in (Тестирование)"
        )
    )
    logs = []

    match check_release_in_jira(jira_connect, BUILD_VERSION):
        case "Not release in Jira":
            logging.info(f'Release {BUILD_VERSION} not find in Jira')
            logs.append(BUILD_VERSION)
            logs.append(
                f'Release not find in Jira'
                '\nPlease check unreleased versions in Jira'
            )

            # Logs table if release NOT in Jira
            table_logs_fail(logs, BUILD_VERSION)

        case True:
            logs.append([
                f'SUCCESS {BUILD_VERSION} find in Jira'
            ])

            for task in all_task:
                match merge(task, BUILD_VERSION):
                    case "Not BUILD_VERSION":
                        # Not in release branch
                        comments_not_in_build_version(jira_connect, task, BUILD_VERSION)
                        logging.info(f'The Merge request in the task ({task}) is not equal to the release version')
                        logs.append([
                            str(task),
                            f'https://jira./browse/{str(task)}',
                            f'RELEASE BRANCH NOT IN: {BUILD_VERSION}.'
                        ])

                    case True:
                        match issuelinks(task, jira_connect, BUILD_VERSION):
                            case "Adding to version":
                                # Adding to version
                                adding_version(jira_connect, task, BUILD_VERSION)
                                logs.append([
                                    str(task),
                                    f'https://jira./browse/{str(task)}',
                                    'Add to version.'
                                ])
                            case [False, None]:
                                # More RFC
                                comments_more_rfc(jira_connect, task, BUILD_VERSION)
                                logs.append([
                                    str(task),
                                    f'https://jira./browse/{str(task)}',
                                    'More RFC detected.'
                                ])

                            case [False, 0]:
                                # Adding to version
                                adding_version(jira_connect, task, BUILD_VERSION)
                                logs.append([
                                    str(task),
                                    f'https://jira./browse/{str(task)}',
                                    'Add to version.'
                                ])

                            case True:
                                # Adding to version
                                adding_version(jira_connect, task, BUILD_VERSION)
                                logs.append([
                                    str(task),
                                    f'https://jira./browse/{str(task)}',
                                    'Add to version.'
                                ])

                            case False:
                                logs.append([
                                    str(task),
                                    f'https://jira./browse/{str(task)}',
                                    'The RFC is not in the right status.'
                                ])

                    case False:
                        # Exception merge to master
                        exception_master(jira_connect, task, BUILD_VERSION)
                        logs.append([
                            str(task),
                            f'https://jira./browse/{str(task)}',
                            f"Exception the task ({task}) was commented out in the master branch."
                        ])

            # Logs table if release in Jira
            table_logs(logs, BUILD_VERSION)








if __name__ == "__main__":
    JIRA_USER = sys.argv[1]
    JIRA_PASSWORD = sys.argv[2]
    BUILD_VERSION = sys.argv[3]

    main(JIRA_USER, JIRA_PASSWORD, BUILD_VERSION)
