from django.apps import AppConfig
'''
用于注册django中的应用
命令行运行：python3 manage.py startapp app_name
其中服务器运行环境中，python用来代指python 2.x, python3 用来代指python3.x
app_name 为所创建应用的名字
注意：1.在创建完一个应用之后，需要在setting的installed_apps列表中进行配置，才能使用该应用
      2.在创建完应用后，同时需要在urls.py中设置相应的路由
'''

class PillboxConfig(AppConfig):
    name = 'pillbox'
