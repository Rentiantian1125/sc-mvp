"""scmvp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from curry import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up', views.sign_up),
    path('sign_in', views.sign_in),
    path('search', views.search),
    path('myself_edit', views.myself_edit),
    path('get_article_list', views.get_article_list),
    path('get_article_content', views.get_article_content),
    path('publish', views.publish),
    path('get_like_and_comment', views.get_like_and_comment),
    path('upload_pic', views.upload_pic),
    path('comment', views.comment),
    path('like', views.like),
    path('get_user_info', views.get_user_info),
]

