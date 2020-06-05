from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.core import serializers
from .models import User, UserAndTheAged, TheAgedAndMedicament
from django.http import HttpResponse
from django.http.response import iJsonResponse
import json
import datetime
from datetime import date
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

'''
在django中，视图是处理逻辑，一个访问请求，通过指定的urls，访问到对应的视图函数
视图接受Web请求，并返回Web响应，响应的内容可能是HTML网页、重定向、404错误、XML文档或图像
等任何东西。在青囊项目中，不涉及到浏览器访问，安卓APP访问和药盒访问只需要涉及到数据
因此，返回的响应以数据为主，多数是为json格式的数据
'''


def hello(request):
    '''
    hello 测试，证明可以访问到服务器，返回欢迎信息
    '''
    return HttpResponse("Hello, this is a http response using django.")


def get_medi(request):
    '''
    处理来自药盒的请求，返回json格式的用药配置
    输入：用户名，密码，老年人信息
    输出：返回json格式的用药配置或当访问出错时返回错误信息
    功能：从数据库中读取响应的数据
    备注：采用POST请求，
    '''
    if request.method == 'POST':
        # 读取用户名
        user_name = request.POST.get('user_name')
        # 读取用户密码
        password = request.POST.get('password')
        try:
            # 尝试从数据库中获得对应用户名的记录
            t = User.objects.get(user_name=user_name)
        except Exception as e:
            # 如果从数据库中获得信息失败，则返回提示读取数据库失败
            return HttpResponse("Something error happened when try to get the record from database, try to upload information from android app.", e)
        # 当成功获取记录时，查看密码是否正确
        if t.password == password:
            try:
                # 当密码正确时读取数据库信息
                m = TheAgedAndMedicament.objects.get(user_name=user_name)
            # 读取失败时返回错误信息
            except Exception as e:
                return HttpResponse("Error happened when try to get the configure of medicament", e)
            # 生成关于服药配置的字典信息
            medi_config = {
                'aged_name': m.aged_name,
                'medicament_name': m.medicament_name,
                'dosage': m.dosage,
                'freq': m.freq,
                'time': str(m.pill_time),  # django中的datetime字段无法自动的生成json，在此将其转化为字符串
                'unit': m.unit,
            }
            # 将服药配置以json格式返回
            return HttpResponse(json.dumps(medi_config))
            
        else:
            # 如果密码错误则返回提示密码错误
            return HttpResponse("Password Error")

    else:
        # 如果不是POST请求，则返回提示，要求以POST访问
        return HttpResponse("Not a POST request, please try again.")


def user(request):
    '''
    处理有关用户的模块，包括注册，登录，修改密码
    输入：用户名，旧密码，fun字段，可选的新密码
    输出：返回包含提示信息的Http响应
    功能：根据fun字段操作数据库中有关用户名和密码的表
    备注：
          fun：
              register，说明是用于注册用户，此时用传入的旧密码作为注册密码，不需要传入新密码
              login，说明是用于登录，从数据库中读取相关记录，查看密码是否正确，返回True或False的Http响应
              reset，用于重置密码，此时旧的密码作为用户名旧密码，当旧密码正确时，用新密码更新，原有旧密码作废
              delete，用于删除在数据库中的该记录，如果密码正确则删除该记录，否则返回提示信息
              其他，返回fun字段无法识别的提示信息
    '''
    if request.method == 'POST':
        user_name = request.POST.get('user_name')

        # 无论是不是修改密码，传入old_password
        old_password = request.POST.get('old_password') 
        fun = request.POST.get("fun")

        # 如果是添加用户名
        if fun == "register":  
            try:
                # 先尝试去注册该用户信息，捕获异常
                User.objects.create(user_name=user_name, password=old_password)  
                return HttpResponse("Registration Success!")
            # 如果注册失败，可能在数据库中已经存在该条信息
            except Exception as e:  
                return HttpResponse("Something error happened. Maybe the user name has been registered, please try another one.", e)
        
        # 如果是用于登录
        elif fun == "login":
            t = User.objects.get(user_name=user_name)
            try:
                if old_password == t.password:
                    # 提示登录成功过
                    return HttpResponse("Login success. Welcome!")
                else:
                    # 提示密码错误，登录失败
                    return HttpResponse("Password Error!!!")
            except Exception as e:  # 如果发生错误
                return HttpResponse("Unknow error happened please try again later or contact the administrator.")

        # 如果是尝试重置密码
        elif fun == "reset":
            new_password = request.POST.get("new_password")
            try:
                t = User.objects.get(user_name=user_name)
                t.password = new_password
                # 保存
                t.save()
            #如果在尝试重置密码时发生错误
            except Exception as e:  
                return HttpResponse("Something error happened when try to reset the password.", e)

        # 如果时尝试删除该条记录
        elif fun == "delete":
            try:
                t = User.objects.get(user_name=user_name)
                t.delete()
            # 如果尝试删除的时候产生错误
            except Exception as e:  
                return HttpResponse("Something error happened when delete the account.", e)
        
        # 如果fun字段不属于以上几类，则属于未识别字段，返回提示信息
        else:
            HttpResponse("Unrecognized fun, please check the request parameters.")

    # 如果不是POST请求，返回提示消息
    else:
        HttpResponse("Not a POST request, something error happened. Please contact the system administrator")


def aged(request):
    '''
    处理有关老年人信息的模块，包括查询老年人信息，删除老年人信息，录入老年人信息
    输入：用户名，密码，fun字段，等必选信息，老年人名字、住址等可选信息
    输出：以提示信息为内容的Http响应
    功能：处理fun字段操作数据库中有关老年人信息的表
    备注：
          fun字段：
                 select，查询老年人信息
                 delete，删除老年人信息
                 change，修改老年人信息，此时需要老年人的全部信息
                 其他情况，录入老年人信息，此时也需要老年人全部信息

    '''
    
    # 判断是否为POST请求
    if request.method == 'POST':  
        user_name = request.POST.get('user_name')
        password_login = request.POST.get('password')
        fun = request.POST.get('fun')
        try:
            # 尝试从数据库中获取该用户
            t = User.objects.get(user_name=user_name)
        # 如果从数据库中获取用户失败，可能的原因是该用户还未被注册
        except Exception as e:
            # 返回提示信息，说明该用户没有被注册
            return HttpResponse("The user has not been register.", e)
        # 如果获取用户名成功，则读取密码
        if t.password != password_login: 
            # 如果密码不正确，返回密码错误的提示消息
            return HttpResponse("Password incorrect.")
        else:  
            # 当密码正确的时候，执行后续的操作

            # 获得老年人的姓名
            aged_name = request.POST.get('aged_name')  

            # 如果是查询，则返回该用户名下所有信息
            if fun == "select":  
                try:
                    t = UserAndTheAged.objects.get(user_name=user_name, aged_name=aged_name)
                except Exception as e:
                    return HttpResponse("Some unknown error happened", e)
                else:
                    return HttpResponse("Result of selection", t)
            
            # 如果是删除
            elif fun == "delete":
                try:
                    t = UserAndTheAged.objects.get(user_name=user_name, aged_name=aged_name)
                except Exception as e:
                    return HttpResponse("Some unknown error happened", e)
                else:
                    t.delete()
                    return HttpResponse("Delete success.")
            
            # 如果不是查询和删除，则说明为录入或修改老年人信息，则需要所有信息
            else:  
                address = request.POST.get('address')
                contact = request.POST.get('contact')
                gender = request.POST.get('gender')
                birth_yy = request.POST.get('birth_yy')
                birth_mm = request.POST.get('birth_mm')
                birth_dd = request.POST.get('birth_mm')
                height = request.POST.get('height')
                weight = request.POST.get('weight')
                emergency_contact_1 = request.POST.get('emergency_contact_1')
                
                # 如果是修改老年人信息
                if fun == "change":
                    try:
                        t = UserAndTheAged.objects.get(user_name=user_name, aged_name=aged_name)
                        t.address = address
                        t.contact = contact
                        t.gender = gender
                        t.birth_yy = birth_yy
                        t.birth_mm = birth_mm
                        t.birth_dd = birth_dd
                        t.emergency_contact_1 = emergency_contact_1
                        t.save()
                    # 修改失败时返回提示消息
                    except Exception as e:
                        return HttpResponse("When change the information of the aged, some error happened", e)
                    # 返回修改成功的提示消息
                    else:
                        return HttpResponse("Information changed success")

                # 其他的情况，则默认是录入老年人信息
                else:
                    # 尝试创建该条记录
                    try:
                        UserAndTheAged.objects.create(user_name=user_name, aged_name=aged_name, address=address, contact=contact,
                                                      gender=gender, birth_yy=birth_yy, birth_mm=birth_mm, birth_dd=birth_dd,
                                                      height=height, weight=weight)
                    # 如果创建失败，则说明可能是该老年人信息已经存在，返回提示消息
                    except Exception as e:
                        return HttpResponse("The elderly has existed in the system.", e)
    
    # 不是POST请求，返回提示消息
    else:
        HttpResponse("Not a POST request, something error happened. Please contact the system administrator")


def medicament(request):
    '''
    处理有关药品信息的模块，包括查询药品信息，删除药品信息，修改药品信息，录入药品信息
    输入：必选参数包括：用户名，密码，老年人名，药品名，可选参数包括：剂量，单位，服药时间，频率等
    输出：包含各种信息的Http响应
    功能：根据输入的fun字段，修改数据库中关于药品信息的表
    备注：
          fun字段：
               select，查询老年人信息
               delete，删除老年人信息
               change，修改老年人信息，此时需要老年人的全部信息
               其他情况，录入老年人信息，此时也需要老年人全部信息
       
    '''

    # 判断是否为POST请求
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password_login = request.POST.get('password')
        fun = request.POST.get('fun')
        try:
            # 先尝试获取该用户
            t = User.objects.get(user_name=user_name)  
        # 获取失败可能时因为该用户没有注册，返回提示信息
        except Exception as e:
            return HttpResponse("The user has not been register.", e)
        # 获取成功时检查密码是否正确
        if t.password != password_login:  # 如果密码不正确
            return HttpResponse("Password incorrect.")
         # 当密码正确的时候
        else:  
            medicament_name = request.POST.get('medicament_name')
            aged_name = request.POST.get('aged_name')  # 获得老年人的信息
            
            # 如果是查询，则返回该用户名下所有信息
            if fun == "select": 
                try:
                    t = TheAgedAndMedicament.objects.get(user_name=user_name, aged_name=aged_name, medicament_name=medicament_name)
                except Exception as e:
                    return HttpResponse("Some unknown error happened", e)
                else:
                    return HttpResponse("Result of selection", t)
            
            # 如果是删除
            elif fun == "delete":
                try:
                    t = TheAgedAndMedicament.objects.get(user_name=user_name, aged_name=aged_name, medicament_name=medicament_name)
                # 删除失败时返回提示消息
                except Exception as e:
                    return HttpResponse("Some unknown error happened", e)
                #删除成功时提示删除成功
                else:
                    t.delete()
                    return HttpResponse("Delete success.")
            
            # 既不是查询，也不是删除，则需要提供所有参数，可能是录入信息或者修改信息
            else:  
                user_name = request.POST.get('user_name')
                aged_name = request.POST.get('aged_name')
                medicament_name = request.POST.get('medicament_name')
                dosage = request.POST.get('dosage')
                unit = request.POST.get('unit')
                freq = request.POST.get('freq')
                pill_time = request.POST.get('pill_time')
                
                # 如果是修改药品信息
                if fun == "change":
                    try:
                        t = TheAgedAndMedicament.objects.get(user_name=user_name, aged_name=aged_name, medicament_name=medicament_name)
                        t.dosage = dosage
                        t.unit = unit
                        t.freq = freq
                        t.pill_time = pill_time
                        t.save()
                    except Exception as e:
                        return HttpResponse("When change the information of the aged, some error happened", e)
                    else:
                        return HttpResponse("Information changed success")
                
                # 对于其他情况，则认为是录入信息
                else:
                    try:
                        TheAgedAndMedicament.objects.create(user_name=user_name, aged_name=aged_name,
                                                            medicament_name=medicament_name, dosage=dosage,
                                                            unit=unit, freq=freq)
                    except Exception as e:
                        return HttpResponse("Something error happened when create the medicament.", e)
                    else:
                        return HttpResponse("The information of medicament added Success!")
    
    # 如果不是POST请求，返回提示信息
    else:
        HttpResponse("Not a POST request, something error happened. Please contact the system administrator")
