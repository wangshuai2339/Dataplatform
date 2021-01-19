from django.db import models

# Create your models here.

class TestUser(models.Model):
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "test_user"
        verbose_name = verbose_name_plural = "测试环境用户信息表"

class TestStar(models.Model):
    starname = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "test_star"
        verbose_name = verbose_name_plural = "测试环境主播信息表"

class User(models.Model):
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "formal_user"
        verbose_name = verbose_name_plural = "正式环境用户信息表"

class Star(models.Model):
    starname = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "formal_star"
        verbose_name = verbose_name_plural = "正式环境主播信息表"

