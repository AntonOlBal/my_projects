from numpy import array


def comments_rfc(jira_connect, task, count, InwardIssue, BUILD_VERSION):
    jira_connect.add_comment(
        task,
        f"Найдена связь ({InwardIssue.raw['fields']['resolution']['name']}) с заявкой ("
        f"{task.raw['fields']['issuelinks'][count]['inwardIssue']['key']}"
        f") в статусе: "
        f"'{task.raw['fields']['issuelinks'][count]['inwardIssue']['fields']['status']['name']}'"
        f"задача, не будет добавлена в релиз {BUILD_VERSION}"
        f" (Сообщение сгенерировано автоматически)"
    )


def comments_more_rfc(jira_connect, task, BUILD_VERSION):
    jira_connect.add_comment(
        task,
        f"Обнаружены связи с несколькими RFC, задача не будет включена в релиз: {BUILD_VERSION}"
        f"(Сообщение сгенерированно автоматически)"
    )


def comments_not_in_build_version(jira_connect, task, BUILD_VERSION):
    jira_connect.add_comment(
        task,
        f"Ошибка не обнаружен merge request в ветку '{BUILD_VERSION}'"
        f"Задача, не будет добавлена в релиз {BUILD_VERSION}"
        f"(Сообщение сгенерированно автоматически)"
    )


def exception_master(jira_connect, task, BUILD_VERSION):
    jira_connect.add_comment(
        task,
        f"ОШИБКА ОБНАРУЖЕН MERGE REQUEST В MASTER ВЕТКУ !"
        f"Задача, не будет добавлена в релиз {BUILD_VERSION}"
        f"(Сообщение сгенерированно автоматически)"
    )


def adding_version(jira_connect, task, BUILD_VERSION):
    all_version = jira_connect.project("FACT")
    for version in all_version.raw['versions']:
       if version['name'] == BUILD_VERSION:
           issue = jira_connect.issue(task)
           # Get all transitions status
           tr = array(jira_connect.transitions(issue))
           for transit in tr:
               # Get transitions id
               if transit['name'] == 'Включить в версию':
                   jira_connect.transition_issue(issue, transit['id'], {'fixVersions': [version]})
