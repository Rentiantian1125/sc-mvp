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


class ArticleContent(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=30)
    img = models.CharField(max_length=30)

    # create_time = models.CharField(max_length=30)

    class Meta:
        db_table = 'article_content'


class ArticleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    article = models.ForeignKey(ArticleContent, on_delete=models.CASCADE, db_constraint=False)

    # create_time = models.TimeField()

    class Meta:
        db_table = 'article_like'


class ArticleComment(models.Model):
    comment = models.CharField(max_length=30)

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    article = models.ForeignKey(ArticleContent, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'article_comment'


class FriendShip(models.Model):
    follow = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, related_name='follow_user')
    fan = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, related_name='fan_user')

    class Meta:
        db_table = 'friendship'
