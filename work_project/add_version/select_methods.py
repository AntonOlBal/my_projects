import numpy as np
import re
import logging

from actions import *


def issuelinks(task, jira_connect, BUILD_VERSION):
    if len(task.raw['fields']['issuelinks']) == 0:
        return "Adding to version"
    return inward(task, jira_connect, BUILD_VERSION)


def inward(task, jira_connect, BUILD_VERSION):
    all_task = []
    rfc = []
    for i in range(len(task.raw['fields']['issuelinks'])):
        try:
            InwardIssue = jira_connect.issue(task.raw['fields']['issuelinks'][i]['inwardIssue']['key'])
            if str(InwardIssue.fields.project.raw['key']).startswith('RFC'):
                all_task.append(True)
                rfc.append(True)
            else:
                all_task.append(False)

        except:
            logging.info(f'Error inwalid objects from inwards {task}')


    if len([i for i, ltr in enumerate(rfc) if ltr]) > 1:
        return [False, None]
    elif len([i for i, ltr in enumerate(rfc) if ltr]) == 0:
        return [False, 0]
    else:
        
        InwardIssue = jira_connect.issue(
            task.raw['fields']['issuelinks'][all_task.index(True)]['inwardIssue']['key']
        )
        logging.info(InwardIssue)
        status = ['Планирование внедрение', 'Планирование внедрения', 'Исполнена', 'Оценка']
        # Check resolution has not null
        if InwardIssue.raw['fields']['resolution'] != '':
            # Get resolution name and compare resolition == 'Отклонено'
            # If the resolution is not equal to 'Отклонено', then we add to the array of statuses, the status is 'Закрыто'
            if InwardIssue.raw['fields']['resolution']['name'] == 'Отклонено':
                logging.info(f"{task} have resolution 'Rejected'")
            status.append('Закрыта')
        status.append('Закрыта')
        
        STATUS_IN = check_status_in(task, status, all_task.index(True), jira_connect, InwardIssue, BUILD_VERSION)
        return STATUS_IN


def check_status_in(task, status, id, jira_connect, InwardIssue, BUILD_VERSION):
    # Inward issue status not in ?
    if task.raw['fields']['issuelinks'][id]['inwardIssue']['fields']['status']['name'] not in status:
        # If the status of the dependent task does not match, write a comment
        # Adding comments
        comments_rfc(jira_connect, task, id, InwardIssue, BUILD_VERSION)
        return False
    else:
        # If the status not in status_types, to task is append to version
        # We go through the versions, find the right one and make the transit of the task to this version
        return True


def merge(task, BUILD_VERSION):
    merge_requests_in_task = np.array(task.raw['fields']['customfield_16581'])
    for merge in merge_requests_in_task:
        if bool(re.match(r'^[0-9]*.[0-9]*.[0-9]* ', f"{merge} ")):
            if merge == BUILD_VERSION:
                to_master = merge_to_master(task)
                return to_master
    return "Not BUILD_VERSION"


def merge_to_master(task):
    merge_requests_in_task = np.array(task.raw['fields']['customfield_16581'])
    for merge in merge_requests_in_task:
        if merge == 'master':
            return False
    return True


def check_release_in_jira(jira_connect, BUILD_VERSION):
    json_all_release_fact = jira_connect.projec_versions("FACT").raw
    for json in json_all_release_fact:
        if str(BUILD_VERSION) == str(json):
            return True
        return 'Not release in Jira'
