from django.http import JsonResponse
from django.shortcuts import HttpResponse
from .models import *
from curry import models
from scmvp.token_service import TokenService
import os


def auth(func):
    def view(request):
        token = TokenService.get_token(request)
        if token:
            user_info = TokenService.check_token(token)
        else:
            return JsonResponse({'code': '1', 'error_msg': '需要登录'})
        return func(request, user_info)

    return view


def sign_up(request):
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

    if name and pwd:
        user_obj = models.User.objects.filter(username=name, password=pwd).first()

        if user_obj:
            return JsonResponse({'code': '0', 'msg': '登录成功',
                                 'token': TokenService.create_token({'id': user_obj.id, 'name': user_obj.username})})
        else:
            return JsonResponse({'code': '1', 'msg': '用户名或密码错误'})
    else:
        return JsonResponse({'code': '1', 'msg': '输入为空'})


def search(request):
    # 按标题搜索
    title = request.POST.get('title')
    if title:
        article_list = ArticleContent.objects.filter(title=title)

        if len(article_list) > 0:
            return JsonResponse({'code': '0', 'msg': '搜索成功', 'article_list': article_list})
        else:
            return JsonResponse({'code': '1', 'msg': '没有匹配项'})
    else:
        return JsonResponse({'code': '1', 'error_msg': '输入为空'})


def myself_edit(request):
    token = TokenService.get_token(request)
    if token:
        user_info = TokenService.check_token(token)
    else:
        return JsonResponse({'code': '1', 'error_msg': '需要登录'})

    user_obj = models.User.objects.filter(id=user_info['id']).first()

    # 修改个人信息
    user_obj.username = request.POST.get('username')
    user_obj.gender = request.POST.get('gender')
    user_obj.nick_name = request.POST.get('nick_name')
    user_obj.phone = request.POST.get('phone')
    user_obj.head_img = request.POST.get('head_img')
    user_obj.sign = request.POST.get('sign')

    user_obj.save()
    return JsonResponse({'code': '0', 'error_msg': '修改成功'})


def get_article_list(request):
    # 获取全部动态内容
    article_list = ArticleContent.objects.all()
    if len(article_list) > 0:
        return JsonResponse({'code': '0', 'msg': '加载成功', 'article_list': article_list})
    else:
        return JsonResponse({'code': '1', 'msg': '无数据'})


@auth
def upload_pic(request):
    file_obj = request.FILES.get('pic')
    file_path = os.path.join('static/images', file_obj.name)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return HttpResponse(file_path)


@auth
def publish(request, user_info):
    # 发表动态
    name = request.POST.get('username')
    title = request.POST.get('gender')
    content = request.POST.get('nick_name')
    img = request.POST.get('img')

    q = models.ArticleContent.objects.create(username=name, title=title, content=content, img=img,
                                             user_id=user_info['id'])
    if q:
        return JsonResponse({'code': '0', 'msg': '发表成功'})
    else:
        return JsonResponse({'code': '1', 'msg': '发表失败'})


@auth
def get_like_and_comment(request, user_info):
    return JsonResponse({
        'code': 0, 'msg': '',
        'like': models.ArticleLike.objects.filter(user_id=user_info['id']),
        'comment': models.ArticleComment.objects.filter(user_id=user_info['id'])
    })
