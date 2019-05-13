from uuid import uuid1
from django.http import JsonResponse
from .models import *
from curry import models
from scmvp.token_service import TokenService
from django.forms.models import model_to_dict
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


@auth
def get_user_info(request, user_info):
    user = User.objects.get(id=user_info['id'])
    return JsonResponse({'code': '0', 'msg': '搜索成功', 'data': model_to_dict(user)})


def search(request):
    # 按标题搜索
    title = request.POST.get('title')
    if title:
        article_list = ArticleContent.objects.values().filter(title=title)

        if len(article_list) > 0:
            return JsonResponse({'code': '0', 'msg': '搜索成功', 'article_list': list(article_list)})
        else:
            return JsonResponse({'code': '1', 'msg': '没有匹配项'})
    else:
        return JsonResponse({'code': '1', 'error_msg': '输入为空'})


@auth
def myself_edit(request, user_info):
    user_obj = models.User.objects.filter(id=user_info['id']).first()

    # 修改个人信息
    user_obj.gender = request.POST.get('gender')
    user_obj.nick_name = request.POST.get('nick_name')
    # user_obj.head_img = request.POST.get('head_img')
    user_obj.sign = request.POST.get('sign')

    user_obj.save()
    return JsonResponse({'code': '0', 'error_msg': '修改成功'})


def get_article_list(request):
    # 获取全部动态内容
    article_list = ArticleContent.objects.values()
    if len(article_list) > 0:
        return JsonResponse({'code': '0', 'msg': '加载成功', 'data': list(article_list)})
    else:
        return JsonResponse({'code': '1', 'msg': '无数据'})


def get_article_content(request):
    token = TokenService.get_token(request)
    user_id = 0 if not token else TokenService.check_token(token)['id']

    article_id = request.POST.get('id')
    article_content = model_to_dict(ArticleContent.objects.get(id=article_id))

    article_comment = ArticleComment.objects \
        .values('article_id', 'comment', 'user__nick_name', 'user__head_img') \
        .filter(article_id=article_id)

    article_content['article_comment'] = list(article_comment)
    article_content['is_like'] = ArticleLike.objects.filter(user_id=user_id, article_id=article_id).count()

    return JsonResponse({'code': '0', 'msg': '加载成功', 'data': article_content})


@auth
def like(request, user_info):
    article_id = request.POST.get('article_id')
    if article_id:
        models.ArticleLike.objects.create(user_id=user_info['id'], article_id=article_id)
        return JsonResponse({'code': '0', 'msg': '点赞成功'})
    else:
        return JsonResponse({'code': '1', 'msg': 'gg'})


@auth
def comment(request, user_info):
    comment_content = request.POST.get('comment')
    article_id = request.POST.get('article_id')
    if comment_content and article_id:
        models.ArticleComment.objects.create(user_id=user_info['id'], article_id=article_id, comment=comment_content)
        return JsonResponse({'code': '0', 'msg': '评论成功'})
    else:
        return JsonResponse({'code': '1', 'msg': 'gg'})


def upload_pic(request):
    file_obj = request.FILES.get('img')
    save_name = str(uuid1()) + os.path.splitext(file_obj.name)[1]
    save_path = 'static/img/'
    file_path = os.path.join(save_path, save_name)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return JsonResponse(
        {'result': '0', 'message': '', 'data': {'url': 'http://127.0.0.1:8000/' + save_path + save_name}})


@auth
def publish(request, user_info):
    # 发表动态
    title = request.POST.get('title')
    content = request.POST.get('content')
    img = request.POST.get('img')

    q = models.ArticleContent.objects.create(title=title, content=content, img=img, user_id=user_info['id'])
    if q:
        return JsonResponse({'code': '0', 'msg': '发表成功'})
    else:
        return JsonResponse({'code': '1', 'msg': '发表失败'})


@auth
def get_like_and_comment(request, user_info):
    return JsonResponse({
        'code': 0, 'msg': '获取成功',
        'like': ArticleLike.objects.select_related('ArticleLike').filter(article__user_id=user_info['id']),
        'comment': ArticleComment.objects.select_related('ArticleComment').filter(article__user_id=user_info['id'])
    })


@auth
def follow(request, user_info):
    user_id = request.POST.get('user_id')
    if user_id:
        models.FriendShip.objects.create(follow_id=user_id, fan_id=user_info['id'])
        return JsonResponse({'code': '0', 'msg': '关注成功'})
    else:
        return JsonResponse({'code': '1', 'msg': 'gg'})
