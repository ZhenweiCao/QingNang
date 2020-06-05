from django.db import models
import django.utils.timezone as timezone
# 本文件是对使用到的数据表格进行定义

'''
django模型使用自带的对象映射关系（Object Relationship Mapping，简称ORM）
用于实现面向对象编程语言里不同系统类型的数据之间的转换
ORM在业务逻辑层和数据库层之间充当了桥梁的作用
ORM是通过使用描述对象和数据库之间的映射的元数据，将程序中的对象自动持久化到数据库中
使用ORM可以提高开发效率，并且可以保证在不同数据库之间平滑切换

在此使用django默认是SQLite数据库
'''

class User(models.Model):  
    '''
    用户名和密码的表，以用户名作为主键
    '''

    # 用户名，主键
    user_name = models.CharField(primary_key=True, max_length=50)
    
    # 密码
    password = models.CharField(max_length=50)


class UserAndTheAged(models.Model): 
    '''
    用户和老年人的表，以用户名和老年人名作为主键，每个老年人设置三个紧急联系人
    '''

    # 用户姓名
    user_name = models.CharField(max_length=50)  
    
    # 监护的老年人姓名
    aged_name = models.CharField(max_length=50)  
    
    # 家庭住址
    address = models.CharField(max_length=200)  
    
    # 联系电话
    contact = models.CharField(max_length=50)  
    
    # 性别，为0为女，为1为男
    gender = models.IntegerField()
    
    # 出生日期：年
    birth_yy = models.IntegerField()
    
    # 出生日期：月
    birth_mm = models.IntegerField()  
    
    # 出生日期：日
    birth_dd = models.IntegerField()
    
    # 身高，单位厘米
    height = models.FloatField()  
    
    # 体重，单位千克
    weight = models.FloatField()  
    
    # 紧急联系人1
    emergency_contact_1 = models.CharField(max_length=20, null=True)
    
    # 紧急联系人2
    emergency_contact_2 = models.CharField(max_length=20, null=True)
    
    # 紧急联系人3
    emergency_contact_3 = models.CharField(max_length=20, null=True)  

    # 将用户名和老年人名作为联合主键
    class Meta:
        unique_together = ('user_name', 'aged_name')


class TheAgedAndMedicament(models.Model):  
    '''
    老年人对应的药品表，以用户名，老年人和药品名为主键，不将药品单独设为一个表，
    因为对于不同的老年人，可能用量不同
    '''
    
    # 用户名
    user_name = models.CharField(max_length=50)
    
    # 老年人名字
    aged_name = models.CharField(max_length=50)
    
    # 药品名
    medicament_name = models.CharField(max_length=50)
    
    # 剂量：即每次服药的数量
    dosage = models.CharField(max_length=50)
    
    #剂量的单位，药品可能为片，或者为成包的颗粒，用来扩展
    unit = models.CharField(max_length=50)  
    
    # 具体的服药时间
    pill_time = models.DateTimeField('TimeToHavePills', auto_now=True)
    
    #服药的间隔时间，可以考虑以分钟为单位，暂不做更多>的扩展
    freq = models.CharField(max_length=50)  

    # 用户名、老年人名、药品名作为联合主键
    class Meta:
        unique_together = ('user_name', 'aged_name', 'medicament_name')


# 扩展数据表，暂时未使用，后续开发可能用到
# 对于药盒，用id来标识每个药盒，对于每个id，唯一而且不重复
class UserAndPillbox(models.Model):
    user_name = models.CharField(primary_key=True, max_length=50)
    pillbox_id = models.CharField(max_length=15)

