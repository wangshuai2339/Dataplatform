from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
from rest_framework.response import Response
from userrole import models
from userrole.serializers import MemeUserSerializer,RoleSerializer
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import time
import json
import datetime
from django.conf import settings
import logging
import pymongo

logger = logging.getLogger('log')


# Create your views here.

# token验证
class AuthticationView(BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):
        token_lifetime = settings.TOKEN_LIFETIME
        token = request.META.get('HTTP_AUTHENTICATION')
        token_obj=models.userToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        else:
            if datetime.datetime.timestamp(datetime.datetime.now()) > (datetime.datetime.timestamp(token_obj.update_time) + token_lifetime):
                token_obj.delete()
                raise exceptions.AuthenticationFailed("token失效")
        return (token_obj.username,token_obj)


# 用户-增（注册）
class Register(APIView):
    authentication_classes = [AuthticationView]
    def post(self, request, *args, **kwargs):
        response = {"code": 0}
        try:
            user = request.data.get("username")
            pas = request.data.get("password")
            nickname = request.data.get("nickname")
            description = request.data.get("description")
            roleid = request.data.get("roleid")
            obj = models.MemeUser.objects.filter(username=user).first()
            if obj:
                response["code"] = "1001"
                response["msg"] = "用户名已经存在"
            else:
                role = models.UserRole.objects.filter(id=roleid).first()
                if role:
                    roleid = models.UserRole.objects.filter(id=role.id).first()
                    models.MemeUser.objects.create(username=user,password=pas,nickname=nickname,description=description,roleid=roleid)
                    response["msg"] = "用户注册成功"
                else:
                    response["code"] = "1001"
                    response["msg"] = "角色名不存在"
        except Exception as e:
            logger.error(e)
            print(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)



# django rest formwork CBV 登录1111
class AuthView(APIView):
    def post(self, request, *args, **kwargs):
        response = {"code": 0}
        try:
            user = request.data.get("username")
            pas = request.data.get("password")

            obj = models.MemeUser.objects.filter(username=user,password=pas).first()

            if not obj:
                response["code"] = "1001"
                response["msg"] = "用户名或密码错误"
                return JsonResponse(response)
            token = str(time.time()) + user
            models.userToken.objects.update_or_create(username=obj,defaults={"token":token})
            response["data"] = {"token": token}

        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)



# 用户-更改
class UserUpdate(APIView):
    authentication_classes = [AuthticationView]
    def put(self,request, *args, **kwargs):
        response = {"code": 0}
        try:
            userid = request.data.get("id")
            user = request.data.get("username")
            pas = request.data.get("password")
            nickname = request.data.get("nickname")
            description = request.data.get("description")
            roleid = request.data.get("roleid")
            token = request.META.get("HTTP_AUTHENTICATION")
            username = models.MemeUser.objects.filter(id=userid)
            if username:
                role = models.UserRole.objects.filter(id=roleid).first()
                if role:
                    username.update(username=user,password=pas,nickname=nickname,description=description,roleid=role.id,update_time=datetime.datetime.now())
                else:
                    response["code"] = "1001"
                    response["msg"] = "角色名不存在"
            else:
                response["code"] = "1001"
                response["msg"] = "用户名不存在"
        except Exception as e:
            print(e)
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)

# 用户-删
class UserDelete(APIView):
    authentication_classes = [AuthticationView]
    def delete(self,request, *args, **kwargs):
        response = {"code": 0}
        try:
            userid = request.GET["userid"]
            username = models.MemeUser.objects.filter(id=userid)
            if username:
                username.delete()
            else:
                response["code"] = "1001"
                response["msg"] = "用户名不存在"
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)

# 用户-查
class UsersInfo(APIView):
    authentication_classes = [AuthticationView]
    def get(self,request, *args, **kwargs):
        response = {"code": 0}
        try:
            response = {'code': 0}
            users = models.MemeUser.objects.all()
            total = models.MemeUser.objects.all().count()
            users = MemeUserSerializer(instance=users, many=True)
            response['data'] = {"total":total,"items":users.data}
        except Exception as e:
            print(e)
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return Response(response)

# 登录用户个人信息
class UserInfo(APIView):
    authentication_classes = [AuthticationView]
    def get(self, request, *args, **kwargs):
        try:
            response = {'code': 0}
            token = request.META.get("HTTP_AUTHENTICATION")
            token_obj=models.userToken.objects.filter(token=token).first()
            logger.info(token_obj)
            logger.info(token_obj.username_id)
            username = models.MemeUser.objects.filter(id=token_obj.username_id).first()
            if username:
                role = models.UserRole.objects.filter(id=username.roleid.id).first()
                logger.info(role)
                response["data"] = {"id": username.id,"realname": username.username, "nickname": username.nickname,"description": username.description, "photo": username.photo,"rolename": str(role.rolename),"rolelimit": str(role.rolelimit), "create_time": str(username.create_time),"update_time": username.update_time}

            else:
                response["code"] = "1001"
                response["msg"] = "用户名不存在"
        except Exception as e:
            print(e)
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)


# 用户角色添加
class RoleAdd(APIView):
    authentication_classes = [AuthticationView]
    def post(self, request, *args, **kwargs):
        response = {"code": 0}
        try:
            rolename = request.data.get("rolename")
            roledes = request.data.get("roledes")
            obj = models.UserRole.objects.filter(rolename=rolename).first()
            if obj:
                response["code"] = "1001"
                response["msg"] = "角色名已经存在"
            else:
                models.UserRole.objects.create(rolename=rolename, roledes=roledes)
                response["msg"] = "角色添加成功"
        except Exception as e:
            print(e)
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)

# 用户角色-查
class RolesInfo(APIView):
    authentication_classes = [AuthticationView]
    def get(self,request, *args, **kwargs):
        response = {"code": 0}
        try:
            response = {'code': 0}
            roles = models.UserRole.objects.all()
            total = models.UserRole.objects.all().count()
            roles = RoleSerializer(instance=roles, many=True)
            response['data'] = {"total":total,"items":roles.data}
        except Exception as e:
            print(e)
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return Response(response)

# 角色-更改
class RoleUpdate(APIView):
    authentication_classes = [AuthticationView]
    def put(self,request, *args, **kwargs):
        response = {"code": 0}
        try:
            roleid = request.data.get("roleid")
            rolename = request.data.get("rolename")
            roledes = request.data.get("roledes")
            roles = models.UserRole.objects.filter(id=roleid)
            if roles:
                roles.update(rolename=rolename,roledes=roledes,update_time=datetime.datetime.now())
            else:
                response["code"] = "1001"
                response["msg"] = "角色名不存在"
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)

# 用户-删
class RoleDelete(APIView):
    authentication_classes = [AuthticationView]
    def delete(self,request, *args, **kwargs):
        response = {"code": 0}
        try:
            roleid = request.GET["roleid"]
            role = models.UserRole.objects.filter(id=roleid)
            if role:
                role.delete()
            else:
                response["code"] = "1001"
                response["msg"] = "角色名不存在"
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)

# 权限编辑
class Roleredact(APIView):
    authentication_classes = [AuthticationView]
    def post(self, request, *args, **kwargs):
        response = {"code": 0}
        try:
            roleid = request.data.get("roleid")
            rolelimit = request.data.get("rolelimit")
            roles = models.UserRole.objects.filter(id=roleid)
            if roles:
                roles.update(rolelimit=rolelimit, update_time=datetime.datetime.now())
            else:
                response["code"] = "1001"
                response["msg"] = "角色名不存在"
        except Exception as e:
            logger.error(e)
            print(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)


# 权限查询
class Rolesearch(APIView):
    authentication_classes = [AuthticationView]
    def get(self, request, *args, **kwargs):
        response = {"code": 0}
        try:
            roleid = request.GET["roleid"]
            roles = models.UserRole.objects.filter(id=roleid).first()
            print(roles.rolelimit)
            if roles:
                response["data"] = {"rolelimit": roles.rolelimit}
            else:
                response["code"] = "1001"
                response["msg"] = "角色名不存在"
        except Exception as e:
            logger.error(e)
            print(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)


# 退出登录
class LoginOut(APIView):
    authentication_classes = [AuthticationView]
    def get(self, request, *args, **kwargs):
        try:
            response = {'code': 0}
            token = request.META.get("HTTP_AUTHENTICATION")
            token_obj=models.userToken.objects.filter(token=token)
            if token_obj:
                token_obj.update(token="",update_time=datetime.datetime.now())
            else:
                response["code"] = "1001"
                response["msg"] = "用户名不存在"
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)


# 修改密码
class PasswordUpdate(APIView):
    authentication_classes = [AuthticationView]
    def post(self, request, *args, **kwargs):
        try:
            response = {'code': 0}
            password = request.data.get("password")
            token = request.META.get("HTTP_AUTHENTICATION")
            token_obj=models.userToken.objects.filter(token=token).first()
            username = models.MemeUser.objects.filter(id=token_obj.username_id)
            if username:
                username.update(password=password, update_time=datetime.datetime.now())
            else:
                response["code"] = "1001"
                response["msg"] = "用户名不存在"
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)



