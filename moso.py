import requests

# 登录
class Loginer:
    def __init__(self, username, passwd, remember='N'):
        '''实例化登录类'''
        self.__username = username
        self.__password = passwd
        self.__remember = remember
        self.__login_url = 'https://www.mosoteach.cn/web/index.php?c=passport&m=account_login'
        self.login_status = None

    @property
    def login(self):
        '''实现登录的操作,用以获取账号的信息'''
        data = {
            'account_name': self.__username,
            'user_pwd': self.__password,
            'remember_me': self.__remember
        }
        try:
            self.login_status = requests.post(self.__login_url, data=data, timeout=5)
            return self.login_status
        except Exception as e:
            print(e)
            return None

    @property
    def get_cookies(self):
        '''以邮箱和手机号的方式登录账号并返回登录成功的cookie值'''
        res = self.login_status
        if res.json()['result_code'] == 0:
            return res.cookies
        else:
            return None

    def get_cookies_phone_capt(self):
        '''待实现'''
        pass

    def show(self):
        res = self.login_status.json()
        username = res['user']['full_name']
        school_name = res['user']['school_name']
        print('%s的%s,你好,欢迎使用!' % (school_name, username))
        # t = input('回车继续>>>')

    def login_phone_capt(self):
        pass
