import sys
import datetime
import os


def get_last_month():
    today = datetime.datetime.today()
    try:
        today = today.replace(month=today.month - 1)
    except ValueError:
        today = today.replace(month=12)
    return '\\' + datetime.datetime.strftime(today, '%B').lower()

def get_file_path_addmonth():
    return get_file_path() + get_last_month()


def get_file_path():
    # 使用命令行指定文件夹名称
    filepath = sys.argv[1]
    return os.path.expanduser('.\\' + filepath)
