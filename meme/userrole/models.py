from django.db import models

# Create your models here.
class UserRole(models.Model):
    rolelimit = models.TextField(max_length=20000,null=True)
    rolename = models.CharField(max_length=32,unique=True)
    roledes = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "role"
        verbose_name = verbose_name_plural = "角色信息表"

class MemeUser(models.Model):
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32)
    description = models.CharField(max_length=32)
    photo = models.CharField(max_length=100,null=True,default="https://test-img-photo.sumeme.com/photo/20847502/1600078804089/2586.jpg")
    roleid = models.ForeignKey(UserRole,to_field="id", on_delete=models.DO_NOTHING,null=True)
    # roleid = models.CharField(max_length=32)
    # rolelimit = models.TextField(max_length=20000,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"
        verbose_name = verbose_name_plural = "用户信息表"

class userToken(models.Model):
    username = models.OneToOneField(to="MemeUser",on_delete=models.CASCADE)
    token = models.CharField(max_length=60)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_token"
        verbose_name = verbose_name_plural = "用户token表"






