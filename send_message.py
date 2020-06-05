'''
该模块为提供发送短信的功能，采用腾讯云提供的短信服务
参考开发者文档：https://cloud.tencent.com/document/product/382/11672
输入：需要提醒的手机号
输出：True or False, 当短信提醒成功时，返回true，若有异常出现导致发送失败，则返回Fasle
      当返回True时，同时打印成功信息，当返回False时，同时打印错误信息
功能：向目标手机号码发送短信
短信内容：尊敬的用户您好，青囊系统检测到您所监护的老人，目前存在危险情况，请您及时查看并确认。青囊致力于为您提供全心全意的服务，感谢您的使用。
短信签名：【zhenwei网】
备注：1.腾讯云短信功能需要认证，因为在此先用同学已备案域名作为签名认证
      2.需要先安装响应依赖包：pip install tencentcloud-sdk-python

'''
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.sms.v20190711 import sms_client, models 
def send_mess():
    try: 
        # 腾讯云SecretId和SecretKey
        cred = credential.Credential("AKIDMXYsLYeEjxwyXtunQmwqY5RWLv2wuyDE", "va1Nk0oZv54vXxh58j45qNdeSA8uRwfR") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = sms_client.SmsClient(cred, "ap-shanghai", clientProfile) 

        req = models.SendSmsRequest()
        
        # 设置发送的手机号，发送短信的模板id，发送短信的签名
        params = '{\"PhoneNumberSet\":[\"+8613792315475\",\"+8613125018788\"],\"TemplateID\":\"615569\",\"Sign\":\"zhenwei网\",\"SmsSdkAppid\":\"1400373765\"}'
        req.from_json_string(params)
        
        # 发送短信
        resp = client.SendSms(req)
       
        # 打印成功之后的发送信息 
        print(resp.to_json_string())
  

    except TencentCloudSDKException as err: 
        # 如果发送遇到错误，则打印错误输出信息
        print(err) 


if __name__=="__main__":
    phone_number = "+8613792315475"
    send_mess()
