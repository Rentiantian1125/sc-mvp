# from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from curry import models
# from rest_framework_jwt.settings import api_settings
from curry.token import Token


def user_save(request):
    user = User(
        username='curry',
        password='123456',
        nick_name='Curry',
        gender='1',
        phone='curry',
        head_img='00000000000.jpg',
        sign='I can do all things'
    )
    user.save()
    return JsonResponse({'code': '0', 'msg': "保存成功"})


def sign_up(request):
    name = 'stephen'
    pwd = '123456'
    re_pwd = '123456'
    gender = '1'

    # name = request.POST.get('username')
    # pwd = request.POST.get('password')
    # re_pwd = request.POST.get('re_pwd')
    # gender = request.POST.get('gender')
    if name and pwd and re_pwd and gender:
        if pwd == re_pwd:
            user_obj = models.User.objects.filter(username=name).first()
            if user_obj:
                return JsonResponse({'code': '1', 'msg': '用户已存在'})
            else:
                models.User.objects.create(username=name, password=pwd, gender=gender).save()
                return JsonResponse({'code': '0', 'msg': "保存成功"})
        else:
            return JsonResponse({'code': '1', 'msg': '密码不一致'})

    else:
        return JsonResponse({'code': '1', 'msg': '输入不能为空'})


def sign_in(request):
    # name = request.POST.get('username')
    # pwd = request.POST.get('password')

    name = 'curry'
    pwd = 'curry'
    token = Token.get_token()

    if name and pwd:
        user_obj = models.User.objects.filter(username=name, password=pwd).first()

        # # 生成token
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # payload = jwt_payload_handler(user_obj)
        # token = jwt_encode_handler(payload)

        if user_obj:
            return JsonResponse({'code': '0', 'msg': '登录成功', 'token': token})
        else:
            return JsonResponse({'code': '1', 'msg': '用户名或密码错误'})
    else:
        return JsonResponse({'code': '1', 'msg': '输入为空'})
