import pytest
import sys
import os


total = {"total_sum": [0, 0, 0, 0, 0]}


def handlers(lin: str):

    """ Функция принимает строку и преобразует ее, сначало в лист,затем в пару ключ/значение для словаря total, и подсчитывает значение для отчета handlers"""

    global total
    line = lin.split(' ')

    if line[3] == "django.request:":
        if (line[2] == "ERROR") and (line[7] not in total):
            total[line[7]] = [0, 0, 0, 0, 0]
        else:
            if (line[5] not in total) and (line[5] != "Server"):
                total[line[5]] = [0, 0, 0, 0, 0]

        if line[2] == 'DEBUG':
            total[line[5]][0] += 1
            total["total_sum"][0] += 1
        if line[2] == 'INFO':
            total[line[5]][1] += 1
            total["total_sum"][1] += 1
        if line[2] == 'WARNING':
            total[line[5]][2] += 1
            total["total_sum"][2] += 1
        if line[2] == 'ERROR':
            total[line[7]][3] += 1
            total["total_sum"][3] += 1
        if line[2] == 'CRITICAL':
            total[line[5]][4] += 1
            total["total_sum"][4] += 1


def test_handlers():
    list_of_lines = ["2025-03-26 12:26:58,000 INFO django.request: GET /admin/login/ 201 OK [192.168.1.81]",
                     "2025-03-26 12:35:57,000 INFO django.request: GET /api/v1/support/ 200 OK [192.168.1.47]",
                     "2025-03-26 12:45:32,000 WARNING django.security: ConnectionError: Failed to connect to payment gateway",
                     "2025-03-26 12:34:49,000 DEBUG django.db.backends: (0.32) SELECT * FROM 'support' WHERE id = 11;",
                     "2025-03-26 12:27:50,000 ERROR django.request: Internal Server Error: /api/v1/auth/login/ [192.168.1.33] - OSError: No space left on device",
                     "2025-03-26 12:12:00,000 DEBUG django.db.backends: (0.34) SELECT * FROM 'reviews' WHERE id = 74;",
                     "2025-03-26 12:34:49,000 DEBUG django.request: GET /admin/login/ 201 OK [192.168.1.81]",
                     "2025-03-26 12:35:57,000 WARNING django.request: GET /api/v1/support/ 200 OK [192.168.1.47]",
                     "2025-03-26 12:34:49,000 CRITICAL django.request: GET /admin/login/ 201 OK [192.168.1.81]",
                     "2025-03-26 12:34:49,000 CRITICAL django.request: GET /admin/login/ 201 OK [192.168.1.81]"]
    total.clear()
    total["total_sum"] = [0, 0, 0, 0, 0]
    for line in list_of_lines:
        handlers(line)
    assert total == {"total_sum": [1, 2, 1, 1, 2],
                     "/admin/login/": [1, 1, 0, 0, 2],
                     "/api/v1/support/": [0, 1, 1, 0, 0],
                     "/api/v1/auth/login/": [0, 0, 0, 1, 0],
                     }


def some_report(lines: str):

    ''' функция для создания нового отчета '''

    pass


def print_table(tot: dict):

    '''функция сортирует словарь в алфавитном порядке и выводит его в виде таблшици'''

    sorted_keys = sorted(tot)
    print(("{:<25} {:<8} {:<8} {:<8} {:<8} {:<10}".format("HEADLER", *["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])))
    for i in sorted_keys:
        print("{:<25} {:<8} {:<8} {:<8} {:<8} {:<10}".format(i, *total[i]))


def do_report(sys_argv: list):

    """Функция принимает аргументы командной строки, открывает фаайл и выполняет отчет в соответсвии с введеным параметром --report"""

    action_flag = sys_argv[-1]

    for arg in range(1, len(sys_argv) - 2):
        with open(sys_argv[arg], "r") as file:
            if action_flag == "handlers":
                for lines in file:
                    handlers(lines)
            if action_flag == "some_action":
                for lines2 in file:
                    some_report(lines2)


def path_check(sys_argv_check: list):

    """Функция проверяет, верно ли указаны пути к файлами, и если хотя бы один не верен возвращает False"""

    for arg in range(1, len(sys_argv_check)-2):
        if not os.path.exists(sys_argv_check[arg]):
            return False
    return True


def test_path_check():
    argv = ["some", "c:/app1.log", "c:/app2.log", "c:/app2.log", "some", "some"]
    argv2 = ["some", "c/a.log", "c/app2.log", "c/app2.log", "some", "some"]
    argv3 = ["some", "c:/a.log", "c:/app2.log", "c:/app2.log", "some", "some"]
    argv4 = ["some", "c:/app1.log", "c:/ap2.log", "c:/app2.log", "some", "some"]
    argv5 = ["some", "c:/app1.log", "c:/app2.log", "c:/ap2.log", "some", "some"]
    assert path_check(argv) == True
    assert path_check(argv2) == False
    assert path_check(argv3) == False
    assert path_check(argv4) == False
    assert path_check(argv5) == False


if __name__ == "__main__":
    if path_check(sys.argv):
        do_report(sys.argv)
        print_table(total)
    else:
        print("Неверно указан путь")
