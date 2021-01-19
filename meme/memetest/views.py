from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
from rest_framework.response import Response
from userrole.views import *
from memetest import models
from memetest.serializers import TestUserSerializer,TestStarSerializer,UserSerializer,StarSerializer
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import time
import json
import datetime
from django.conf import settings
import logging
import pymongo
# from userrole.views import AuthticationView

logger = logging.getLogger('log')


# Create your views here.

# 测试用户11
class TuserView(APIView):
    authentication_classes = [AuthticationView]
    def get(self, request, *args, **kwargs):
        try:
            response = {'code': 0}
            tusers = models.TestUser.objects.all()
            total = models.TestUser.objects.all().count()
            testusers = TestUserSerializer(instance=tusers, many=True)
            response['data'] = {"total":total,"items":testusers.data}
        except Exception as e:
            print(1)
            print(e)
            print(2)
            logger.error(e)
            print(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return Response(response)


# 测试主播
class TstarView(APIView):
    authentication_classes = [AuthticationView]
    def get(self, request, *args, **kwargs):
        try:
            response = {'code': 0}
            tstars = models.TestStar.objects.all()
            total = models.TestStar.objects.all().count()
            teststars = TestStarSerializer(instance=tstars, many=True)
            response['data'] = {"total":total,"items":teststars.data}
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return Response(response)


# 线上用户
class UserView(APIView):
    authentication_classes = [AuthticationView]
    def get(self,request, *args, **kwargs):
        try:
            response = {"code": 0}
            users = models.User.objects.all()
            total = models.User.objects.all().count()
            users = UserSerializer(instance=users, many=True)
            response['data'] = {"total": total, "items": users.data}
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return Response(response)

# 线上主播
class StarView(APIView):
    authentication_classes = [AuthticationView]
    def get(self,request, *args, **kwargs):
        try:
            response = {"code": 0}
            stars = models.Star.objects.all()
            total = models.Star.objects.all().count()
            stars = StarSerializer(instance=stars, many=True)
            response['data'] = {"total": total, "items": stars.data}
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return Response(response)


# 创建测试服新用户
class CreateUser(APIView):
    authentication_classes = [AuthticationView]
    def post(self,request, *args, **kwargs):
        response = {"code": 0}
        username = request.data.get("username")
        pwd = request.data.get("password")
        datas = {"username":username,"pwd":pwd}
        url = "https://test-user.memeyule.com/register/robot"
        ret = requests.get(url,params=datas)
        try:
            if ret.json()["code"] == 30408:
                msg = ret.json()["error"]
                response["msg"] = msg
                response["code"] = 1001
            elif ret.json()["code"] == 1:
                response["data"] = {"username":username,"password":pwd}
                response["msg"] = "新用户创建成功"
            else:
                response["code"] = "1002"
                response["msg"] = "请求异常"
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)


# 测试充值
class TestPay(APIView):
    authentication_classes = [AuthticationView]
    def post(self,request, *args, **kwargs):
        response = {"code": 0}
        id = request.data.get("id")
        cny = request.data.get("cny")
        datas = {"id": id, "cny": cny,"via":"HUAWEI"}
        url = "https://test-api.memeyule.com/pay/test_success_pay"
        ret = requests.get(url, params=datas)
        try:
            if ret.json()["code"] == 1:
                response["data"] = {"userid":id,"money":(cny+" 元")}
                response["msg"] = "充值成功%s"%(cny+" 元")
            else:
                response["code"] = "1002"
                response["msg"] = "请求异常"
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)


# 多人pk自动发起
class MultiPk(APIView):
    authentication_classes = [AuthticationView]
    def post(self, request, *args, **kwargs):
        response = {"code": 0 ,"msg": "匹配成功"}
        user_index1 = request.data.get("user_index1")
        user_index2 = request.data.get("user_index2")
        user_index3 = request.data.get("user_index3")
        user_index4 = request.data.get("user_index4")
        user_list = [user_index1, user_index2, user_index3, user_index4]
        user_token = {}

        # 主播登录
        try:
            for username in user_list:
                data_auth = {"username": username, "password": "654321", "grant_type": "password", "scope": "PC_WEB"}
                url = "https://test-amber.memeyule.com/api/v1/oauth2/token"
                ret = requests.post(url, data=data_auth)
                access_token = ret.json()["access_token"]
                user_token[username] = access_token
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"

        # 邀请主播
        try:
            for i in range(3):
                # data_invite = {"uid": user_list[i + 1], "index": i + 2, "assign_room_id": 20990170}
                data_invite = {"uid": user_list[i + 1], "index": i + 2}
                token_index = user_token[user_list[0]]
                url = "https://test-cryolite.memeyule.com/api/v5/multi-pk/invite?access_token=" + token_index
                ret = requests.post(url, data=json.dumps(data_invite))
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"


        # 接受接口
        try:
            for token in user_token:
                # print(user_token[token])
                data_invite = {"uid": user_list[0], "type": 1}
                token_index1 = user_token[token]
                url = "https://test-cryolite.memeyule.com/api/v5/multi-pk/handle-invite?access_token=" + token_index1
                ret = requests.post(url, data=json.dumps(data_invite))
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"

        return JsonResponse(response)



# 主播发起随机匹配
class LadderPk(APIView):
    authentication_classes = [AuthticationView]
    def post(self, request, *args, **kwargs):
        response = {"code": 0 ,"msg": "发起匹配"}
        user_index1 = request.data.get("user_index1")
        user_index2 = request.data.get("user_index2")
        user_index3 = request.data.get("user_index3")
        user_list = [user_index1, user_index2, user_index3]
        user_token = []
        try:
            for username in user_list:
                # 查询主播token
                myclient = pymongo.MongoClient(host="192.168.31.229",port=10000)
                mydb = myclient["xy_user"]["users"]
                myc1 =mydb.find_one({"mm_no": username})
                user_token.append(myc1["token"])
                # 修改主播的开播状态
                myclient = pymongo.MongoClient(host="192.168.31.229",port=26000)
                mydb = myclient["xy"]["rooms"]
                myquery = {"_id":int(username)}
                newvalues = {"$set": {"live":True}}
                mydb.update_one(myquery, newvalues)
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        # 主播随机匹配
        try:
            print(user_token)
            logger.info(user_token)
            for i in range(3):
                token_index = user_token[i]
                url = "https://test-cryolite.memeyule.com/api/v5/multi-pk/ladder/match?access_token=" + token_index
                print(url)
                ret = requests.post(url)
        except Exception as e:
            logger.error(e)
            response["code"] = "1002"
            response["msg"] = "请求异常"
        return JsonResponse(response)