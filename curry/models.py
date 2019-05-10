from django.db import models


# Create your models here.
class User(models.Model):
    # id = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    nick_name = models.CharField(max_length=30)
    gender = models.SmallIntegerField()
    phone = models.CharField(max_length=30)
    head_img = models.CharField(max_length=30)
    sign = models.CharField(max_length=150)

    # create_time = models.TimeField()

    class Meta:
        db_table = 'user'


class ArticleLike(models.Model):
    article_id = models.IntegerField()
    user_id = models.IntegerField()
    # create_time = models.TimeField()

    class Meta:
        db_table = 'article_like'


class ArticleComment(models.Model):
    article_id = models.IntegerField()
    # user_id = models.IntegerField()
    comment = models.CharField(max_length=30)
    # create_time = models.TimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)

    # user = models.ForeignKey(User, to_field=User.id, db_constraint=False, on_delete=None)
    # user = models.ForeignKey(User, to_field=User.id, db_constraint=False, on_delete=None)
    # comment_user = models.OneToOneField("User", on_delete=None)

    class Meta:
        db_table = 'article_comment'


class ArticleContent(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=30)
    img = models.CharField(max_length=30)

    # create_time = models.CharField(max_length=30)

    class Meta:
        db_table = 'article_content'
