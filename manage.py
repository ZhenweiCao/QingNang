#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
'''
django在命令行执行的脚本，用于启动django服务，更新数据库等操作

以服务器ip启动服务器，开放端口为8000： 
python3 manage.py runserver 0.0.0.0:800

用shell进行交互（可以将服务器运行在后台，这样不影响shell）
启动shell：
python3 manage.py shell
进入python交互之后
>>>from pillbox.models import *    # 这条python语句可以将数据库里创建的表格包含进来
>>>t = User.objects.all()    # User为pillbox/modesl.py里的User对象，对应与数据库里用户名和用户>名密码的表。返回的t为存储数据库中User类型对象的列表
>>>tmp_user = User.objects.get(user_name='zhenwei')    # 从数据库中获取user_name为'zhenwei'的对
象，这里user_name为主键，不可修改，不可重复
>>>tmp_user.password    # tmp_user对象的password属性，对应用户名和用户密码的表里用户名为’zhenwei‘的记录对应的密码
>>>tmp_user_add = User.objects.create(user_name='test_user_name', password='test_password')    # 创建一个用户名和密码的记录，返回创建记录的对象


重新生成数据库
python3 manage.py makemigrations
python3 manage.py migrate

'''
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QingNang.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
