import random

from django.core.mail import send_mail

from MxOnline.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def send_register_email(email_addr, send_type='register'):
    if send_type == 'changeemail':
        code = random_code(4)
    else:
        code = random_code(10)

    email_verify_record = EmailVerifyRecord()
    email_verify_record.code = code
    email_verify_record.email = email_addr
    email_verify_record.send_type = send_type
    email_verify_record.save()

    if send_type == 'register':
        email_title = '慕学在线注册用户激活'
        email_body = '这是慕学在线注册用户激活邮件，请点击如下链接以激活用户：http://127.0.0.1:8000/user/active/{0}'.format(code)
        status = send_mail(email_title, email_body, EMAIL_FROM, [email_addr])
    elif send_type == 'forget':
        email_title = '慕学在线密码重置'
        email_body = '这是慕学在线用户重置密码链接，请点击如下链接以重置密码：http://127.0.0.1:8000/user/reset/{0}'.format(code)
        status = send_mail(email_title, email_body, EMAIL_FROM, [email_addr])
    elif send_type == 'changeemail':
        email_title = '慕学在线邮箱重置'
        email_body = '这是慕学在线用户重置邮箱验证码：{0}'.format(code)
        status = send_mail(email_title, email_body, EMAIL_FROM, [email_addr])
    return status


def random_code(len=6):
    ''' 随机生成6位的验证码 '''
    # 注意： 这里我们生成的是0-9A-Za-z的列表，当然你也可以指定这个list，这里很灵活
    # 比如： code_list = ['P','y','t','h','o','n','T','a','b'] # PythonTab的字母
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        code_list.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        code_list.append(chr(i))
    myslice = random.sample(code_list, len)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)  # list to string
    return verification_code