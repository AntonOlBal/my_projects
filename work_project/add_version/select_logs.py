from prettytable import PrettyTable, ALL, PLAIN_COLUMNS
import codecs


def table_logs(data, BUILD_VERSION):
    logs_task_table = PrettyTable(encoding="utf-8")
    logs_task_table.title = f"ADDING TO THE VERSION {BUILD_VERSION}"
    logs_task_table.align[f"ADDING TO THE VERSION {BUILD_VERSION}"] = "c"
    logs_task_table.field_names = ["TASK", "URL", "ACTIONS"]
    logs_task_table.align["TASK"] = "c"
    logs_task_table.align["FILES"] = "c"
    logs_task_table.align["ACTIONS"] = "c"
    logs_task_table.valign = "m"
    logs_task_table.hrules = ALL
    logs_task_table.vrules = ALL
    for logs in data:
        logs_task_table.add_row([str(logs[0]), str(logs[1]), str(logs[2])])

    print(str(logs_task_table))


def table_logs_fail(data, BUILD_VERSION):
    logs_task_table = PrettyTable(encoding="utf-8")
    logs_task_table.title = f"FAIL ADDING TO THE VERSION {BUILD_VERSION}"
    logs_task_table.align[f"FAIL ADDING TO THE VERSION {BUILD_VERSION}"] = "c"
    logs_task_table.field_names = ["RELEASE", "ERROR"]
    logs_task_table.align["RELEASE"] = "c"
    logs_task_table.align["ERROR"] = "c"
    logs_task_table.hrules = ALL
    logs_task_table.vrules = ALL
    logs_task_table.add_row([str(data[0]), str(data[1])])

    print(str(logs_task_table))

