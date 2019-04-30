# from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from curry import models


# from rest_framework_jwt.settings import api_settings


def sign_up(request):
    # name = 'stephen'
    # pwd = '123456'
    # re_pwd = '123456'
    # gender = '1'

    name = request.POST.get('username')
    pwd = request.POST.get('password')
    re_pwd = request.POST.get('re_pwd')
    gender = request.POST.get('gender')
    if name and pwd and re_pwd and gender:
        if pwd == re_pwd:
            user_obj = models.User.objects.filter(username=name).first()
            if user_obj:
                return JsonResponse({'code': '1', 'msg': '用户已存在'})
            else:
                models.User.objects.create(username=name, password=pwd, gender=gender)
                return JsonResponse({'code': '0', 'msg': "保存成功"})
        else:
            return JsonResponse({'code': '1', 'msg': '密码不一致'})

    else:
        return JsonResponse({'code': '1', 'msg': '输入不能为空'})


def sign_in(request):
    name = request.POST.get('username')
    pwd = request.POST.get('password')

    # name = 'curry'
    # pwd = '123456'

    if name and pwd:
        user_obj = models.User.objects.filter(username=name, password=pwd).first()

        # # 生成token
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # payload = jwt_payload_handler(user_obj)
        # token = jwt_encode_handler(payload)

        if user_obj:
            return JsonResponse({'code': '0', 'msg': '登录成功', 'token': user_obj.id})
        else:
            return JsonResponse({'code': '1', 'msg': '用户名或密码错误'})
    else:
        return JsonResponse({'code': '1', 'msg': '输入为空'})


def search(request):
    # 按标题搜索
    title = request.POST.get('title')
    if title:
        article_list = ArticleContent.objects.all().filter(title=title)

        if len(article_list) > 0:
            return JsonResponse({'code': '0', 'msg': '搜索成功', 'article_list': article_list})
        else:
            return JsonResponse({'code': '1', 'msg': '没有匹配项'})

    else:
        return JsonResponse({'code': '1', 'error_msg': '输入为空'})


def myself_edit(request):
    # 修改个人信息
    name = request.POST.get('username')
    gender = request.POST.get('gender')
    nick_name = request.POST.get('nick_name')
    phone = request.POST.get('phone')
    head_img = request.POST.get('head_img')
    sign = request.POST.get('sign')

    models.User.objects.create(username=name, gender=gender, nick_name=nick_name,
                               phone=phone, head_img=head_img, sign=sign)


def get_article_list(request):
    # 获取全部动态内容
    article_list = ArticleContent.objects.filter()
    # article_list = ArticleContent.objects.all()
    if len(article_list) > 0:
        return JsonResponse({'code': '0', 'msg': '加载成功', 'article_list': article_list})
    else:
        return JsonResponse({'code': '1', 'msg': '无数据'})


def publish(request):
    # 发表动态
    name = request.POST.get('username')
    title = request.POST.get('gender')
    content = request.POST.get('nick_name')
    img = request.POST.get('phone')

    q = models.ArticleContent.objects.create(username=name, title=title, content=content, img=img)
    if q:
        return JsonResponse({'code': '0', 'msg': '发表成功'})
    else:
        return JsonResponse({'code': '1', 'msg': '发表失败'})


def get_like_and_comment(request, user_id):
    # 获取用户收到的点赞及评论信息
    models.ArticleLike.objects.filter(user_id=user_id)
    # models.ArticleLike.objects.all().filter(user_id=user_id)
    models.ArticleComment.objects.filter(user_id=user_id)
