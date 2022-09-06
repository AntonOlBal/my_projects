import datetime
import re
import os


def check_correct_input(some_path_to_folder: str) -> str | bool:
    special_sym = "+=[]:*?;«,./\<>| "
    start_path = '/data/current/snapshots'

    if some_path_to_folder not in special_sym and some_path_to_folder.startswith(start_path):
        return some_path_to_folder
    else:
        return False


# create list_date which not remove.
# создание list_date которые не нужно удалять
today = datetime.date.today()
day_delta = 0
list_date = []
while day_delta <= 11:
    tmp = today - datetime.timedelta(day_delta)
    list_date.append(str(tmp))
    day_delta += 1

# Creating a file with paths to databases.
# Создание файла с путями до инкрементов баз данных
path_to_folder = input(str("Enter the path to the directory with increments. "
                            "Example: data/current/snapshots/folder_name"))
os.system(f'-ls -l {path_to_folder} > all_DB.txt')

# create file with old DB and create file with commands for delete old DB.
# создание файла с устаревшими БД и создание файла с командами для удаления устаревших БД
with open('all_DB.txt', 'r') as all_DB, \
        open('cmd_to_clean.sh', 'w') as cmd_to_clean:
    for removed_delta in all_DB:
        # Removing excess from ls output.
        # Удаление лишнего из вывода ls
        tmp_DB = removed_delta.replace('drwxrwx--x+  - hive hive          0 ', '')
        # Excluding empty, extra lines and dates that do not need to be removed
        # Исключая пустые, лишние строки и даты, которые не нужно удалять
        if tmp_DB[:10] not in list_date:
            if len(tmp_DB) > 0 and not tmp_DB.startswith('Found'):
                # Search mask
                # Маска поиска.
                pattern = r'(\w+\S+)'
                tmp_elem = re.findall(pattern, tmp_DB)
                if check_correct_input(path_to_folder):
                    cmd_to_clean.write('-rm -f ' + path_to_folder + str(tmp_elem[0]) + '\n')
                else:
                    print('The path must start from ' + start_path + ' and not have special symbols')
        break

os.system('chmod +x cmd_to_clean.sh ; '
          'echo ALL DB OLDER THAN 11 DAYS WILL BE REMOVED ; echo 3 ; sleep 2 ; echo 2 ; sleep 2 ; echo 1 ; '
          'sleep 2 ; ./cmd_to_clean.sh ; rm cmd_to_clean.sh')
