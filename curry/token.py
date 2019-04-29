import hashlib
import time


# 创建获取时间戳的对象
class Time(object):
    def t_stamp(self):
        t = time.time()
        t_stamp = int(t)
        print('当前时间戳:', t_stamp)
        return t_stamp


# 创建获取token的对象
class Token(object):
    def __init__(self, api, username, password):
        self._API_SECRET = api
        self.project_code = username
        self.account = password

    def get_token(self):
        strs = self.project_code + self.account + str(Time().t_stamp()) + self._API_SECRET
        hl = hashlib.md5()
        hl.update(strs.encode("utf8"))  # 指定编码格式，否则会报错
        token = hl.hexdigest()
        # print('MD5加密前为 ：', strs)
        print('MD5加密后为 ：', token)
        return token


if __name__ == '__main__':
    tokenprogramer = Token('api具体值', 'username具体值', 'password具体值')  # 对象实例化
    tokenprogramer.get_token()  # 调用token对象
