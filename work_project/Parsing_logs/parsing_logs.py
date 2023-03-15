#Script for find errors in logs
#-*- coding: utf-8 -*- #Нужно заменить кодировку на виндовую!!! cp 1251, оставил ютф чтобы было видно комменты в гит
#При переносе скрипта в билдер ко всем "%" в скрипте, добавить еще один "%" !!!
import re
import sys
import os
import datetime

name_log = str(sys.argv[2])
path_to_folder_logs = str(sys.argv[1])

#TEST
#name_log = '5.06.2980.001_ina02.log'
#path_to_folder_logs = 'C:/folder'

reg_exp_error = r'pls-|ORA-|WARRING|SP2-|Предупреждение|Ошибки|must be declared|compilation errors.$|с ошибками компиляции.$'
reg_exp_dublicate_error = r'^Errors for .{1,70}:$|^Ошибки для .{1,70}$'
start_issue = r'===== ЗАДАЧА  NA-(.*)'
end_issue = r'End: d:\\svn(.*)'
name_script = r'Start: d:\\svn\\ABS'
time_start = r'^Time start '
time_end = r'^Time end '



# Переменные для фиксации номеров строк: Начала, ошибки, конца, времени выполнения
num_start_issue = 0
num_line_comp_er = 0
num_end_issue = 0
num_line_dubl_er = 0
num_name_script_line = 0
num_time_start = 0
num_time_end = 0

with open(f'{path_to_folder_logs}/{name_log}', 'r') as file_log:
    #Счетчик текущего номера строки
    num_lines = 0
    #Результат - уникальные ошибки
    result = ''
    #Сюда пишутся скрипты выполняемые более 5 минут
    long_run_time = ''
    #Чтение лога построчно
    lines = file_log.readlines()
    for line in lines:
        num_lines += 1
        #Поиск и факсация  номера строки начала.
        #Учитываем, что может быть ошибка ДО старта прогона по задачам
        #Учитываем, что строка End, может отсутствовать
        if re.findall(start_issue, line):
            if num_line_comp_er != 0 and num_start_issue == 0:
                result += '\n==========================================================\n' \
                          'ERROR! Ошибки ДО старта прогона задач\n' \
                          'Возможно при настройке триггера  DDL и DisableSpravSync\n' \
                          f'Проверьте основной лог - {name_log}\n' \
                          '==========================================================\n'
                num_line_comp_er = 0
            if num_line_comp_er != 0 and num_start_issue != 0:
                result += '\n==========================================================\n' \
                          'ERROR! Отсутствует строка "End:" в логе задачи:\n' \
                          f'{lines[num_start_issue]}' \
                          f'Не хватает "/" в конце скрипта:\n' \
                          f'{lines[num_name_script_line].partition("Start: ")[2]}' \
                          '==========================================================\n'
                num_line_comp_er = 0
            num_start_issue = num_lines - 1
        # Поиск и факсация времени начала скрипта
        if re.findall(time_start, line):
            num_time_start = num_lines - 1
        # Поиск и факсация имени скрипта
        if re.findall(name_script, line):
            num_name_script_line = num_lines - 1
        # Поиск и факсация  номера строки с ошибкой, которая возможно дублируется
        if re.findall(reg_exp_dublicate_error, line):
            num_line_dubl_er = num_lines - 1
        #Поиск и факсация  номера строки с ошибкой
        if re.findall(reg_exp_error, line):
            num_line_comp_er = num_lines - 1
        #Поиск и факсация  номера строки конца
        if re.findall(end_issue, line):
            num_end_issue = num_lines - 1
        # Поиск и факсация времени конца скрипта, запись все скриптов дольше 5 минут в long_run_time
        if re.findall(time_end, line):
            num_time_end = num_lines - 1
            if num_time_start and num_time_end != 0:
                time_start_issue = datetime.datetime.strptime(lines[num_time_start].lstrip('Time start '),
                                                              '%d/%m/%Y %H:%M:%S ') #При переносе в билдер добавить еще %
                time_end_issue = datetime.datetime.strptime(lines[num_time_end].lstrip('Time end '),
                                                            '%d/%m/%Y %H:%M:%S ') #При переносе в билдер добавить еще %
                delta_run = time_end_issue - time_start_issue
                if delta_run > datetime.timedelta(minutes=5):
                    long_run_time += f'\nЗадача: {lines[num_start_issue]}' \
                                     f'Скрипт: {lines[num_name_script_line].partition("Start: ")[2]} Выполнялся: ' \
                                     f'{delta_run}\n'
            #Запись в result от начла до конца, только если была ошибка и она не дублируется
            if num_start_issue and num_line_comp_er and num_end_issue and num_line_dubl_er != 0:
                if lines[num_line_dubl_er] not in result:
                    for line_er in range(num_start_issue - 1, num_end_issue + 1):
                        result += lines[line_er]
                #Проверка тела лога на ошибки, если было "ЭХО" num_line_dubl_er != 0
                else:
                    err_bdy = 0
                    for line_er_bdy in range(num_start_issue - 1, num_line_dubl_er):
                        if re.findall(reg_exp_error, lines[line_er_bdy]):
                            err_bdy = 1
                    if err_bdy == 1:
                        # Если была ошибка, добавить тело лога, ДО эхо
                        for line_er_bdy in range(num_start_issue - 1, num_line_dubl_er):
                            result += lines[line_er_bdy]
                        result += lines[num_end_issue]
            # Запись в result от начала до конца, только если была ошибка и она не может дублироваться
            elif num_start_issue and num_line_comp_er and num_end_issue != 0:
                for line_er in range(num_start_issue - 1, num_end_issue + 1):
                    result += lines[line_er]
            # Перевод переменных в 0 после каждой задачи
            num_line_dubl_er = 0
            num_start_issue = 0
            num_line_comp_er = 0
            num_end_issue = 0
            num_name_script_line = 0
            num_time_start = 0
            num_time_end = 0

    #Если был один скрипт ВСЕГО и у него отсутсвует End или ENDA нет в последней задаче
    if num_line_comp_er != 0 and num_start_issue != 0:
        result += '\n==========================================================\n' \
                  'ERROR! Отсутствует строка "End:" в логе задачи:\n' \
                  f'{lines[num_start_issue]}' \
                  f'Не хватает "/" в конце скрипта:\n' \
                  f'{lines[num_name_script_line].partition("Start: ")[2]}' \
                  '==========================================================\n'

#Формирование файла ERROR_*.log, перетирание если такой уже был
if not os.path.isdir(f'{path_to_folder_logs}/ERRORS'):
    os.mkdir(f'{path_to_folder_logs}/ERRORS')
with open(f'{path_to_folder_logs}/ERRORS/ERROR_{name_log}', 'w', encoding='cp1251') as log_error_file:
    if result == '':
        log_error_file.write('\n========================================================================\n'
                             f'====== В тексте лога - {name_log} ОШИБОК НЕ НАЙДЕНО =======\n'
                             '========================================================================\n')
    else:
        log_error_file.write(result)
    log_error_file.write(f'\n=========== Скрипты выполняющиеся более 5 минтут ====================\n'
                         f'\n')
    if long_run_time == '':
        log_error_file.write(f'\nВ логе {name_log} длительных скриптов НЕ ОБНАРУЖЕНО\n'
                             f'\n')
    else:
        log_error_file.write(long_run_time)
