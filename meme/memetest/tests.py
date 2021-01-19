from django.test import TestCase
import requests
import json
from django.http import HttpResponse,JsonResponse
import os,django
import pymongo
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meme.settings")# project_name 项目名称
django.setup()
import re
import time
import datetime
import settings
from memetest import models
# Create your tests here.

# 批量创建用户
# def CreateUser():
#     for i in range(21):
#         ghid = "gh000" + str(i+1)
#         username = ghid
#         pwd = "123456"
#         datas = {"username": username, "pwd": pwd}
#         url = "https://test-user.memeyule.com/register/robot"
#         ret = requests.get(url, params=datas)
#         try:
#             if ret.json()["code"] == 30408:
#                 msg = ret.json()["error"]
#                 response = msg
#                 print(response)
#             elif ret.json()["code"] == 1:
#                 response = "新用户创建成功" + str(i+1)
#                 print(response)
#             else:
#                 response = "请求异常"
#         except Exception as e:
#             response = "请求异常"
#             print(response)
# a = CreateUser()
# print(a)

# a=[]
# # 验证用户是否创建成功(获取token)
# for i in range(21):
#     ghid = "gh000" + str(i+1)
#     username = ghid
#     data_auth = {"username": username, "password": "123456", "grant_type": "password", "scope": "PC_WEB"}
#     url = "https://test-amber.memeyule.com/api/v1/oauth2/token"
#     ret = requests.post(url, data=data_auth)
#     access_token = ret.json()["access_token"]
#     a.append(access_token)
#     user_token = ("%s的token是%s")%(ghid,access_token)
#     print(user_token)
# print(a)

# # 批量造公会
# for i in range(21):
#     ghid = "公会000" + str(i+1)
#     username = ghid
#     data_auth = {"name": username,"star_num": 3,"exp": "true","real_name": username,"sex": 0,"qq": "123456","tel": "123456","sfz": "123456","bank": "123456","bank_location": "123456","bank_user_name": "123456","bank_id": "123456","bank_user_mobile": "123456","bank_user_sfz": "123456","bank_user_sfz_pic1": "123456","bank_user_sfz_pic2": "123456"}
#     url = "https://test-cryolite.memeyule.com/api/v1/guild/apply?access_token=" + a[i]
#     ret = requests.post(url, data=json.dumps(data_auth))
#     print(ret)
#     print(i+1)

# 查询公会
# url="https://test-cryolite.memeyule.com/api/v1/guild/list"
# ret = requests.get(url)
# print(ret.json()["items"])

# 批量送礼
# for i in range(21):
#     url = "https://test-api.memeyule.com/room/send_gift/"+a[i]+"/20853421/863?count=1000&user_id=20853421&marquee=yes&_=1605777283364"
#     requests.get(url)
#     print(i+1)

# 实名认证
# def user_identity_auth(request):
#     if request.method == 'GET':
#         uid = request.GET.get('uid')
#         name = request.GET.get('name')
#         sfid = request.GET.get('sfid')
#         myclient = pymongo.MongoClient(host="192.168.31.229", port=26000)
#         mydb = myclient["xy"]["user_identity_auth"]
#         myc1 = mydb.find_one({"uid": int(uid)})
#         print(myc1)
#         if not myc1 is None:
#             myc2 = myc1["uid"]
#             print(1)
#             if int(uid) == myc2:
#                 response = {'code': 1003, 'msg': "已经实名认证成功，请勿重新认证"}
#         else:
#             try:
#                 en_idCardNumber = "73217FC5D506BDA6067DA373BC11581BE0686406030C2" + str(sfid)
#                 mydict = {"uid": int(uid), "en_idCardNumber": en_idCardNumber, "name": str(name),
#                           "timestamp": 1601000799391}
#                 x = mydb.insert_one(mydict)
#                 print(x.inserted_id)
#                 myc1 = mydb.find_one({"uid": 20853489})
#                 myc2 = myc1["uid"]
#                 print(myc1)
#                 print(myc2)
#                 if int(uid) == int(myc2):
#                     response = {'code': 1000, 'msg': "实名认证成功"}
#                 else:
#                     response = {'code': 1002, 'msg': "实名认证落库失败"}
#             except Exception as exc:
#                 print(exc)
#                 response = {'code': 1001, 'msg': "身份证号重复"}
#         return JsonResponse(response)
#



# 数据库多层对象修改

# myclient = pymongo.MongoClient(host="192.168.31.229", port=26000)
# mydb = myclient["xy"]["users"]
# myc1 = mydb.find_one({"_id": 1492303})
# # myc1 = mydb.find_one({"_id":1492303,"star.broker":1201107})
# print(myc1)
# print(type(myc1))
# print(myc1["star"]["broker"])
# print(type(myc1["star"]["broker"]))
#
#
#
# myquery = {"_id":1492303,"star.broker":1201107}
# newvalues = {"$set": {"star.broker":123456}}
#
# mydb.update_one(myquery, newvalues)


# a = [20883701, 21014300, 21014301, 21014313, 21014314, 21014315, 21014316, 21014317, 21014318, 21014319, 21014320,
#      21014321, 21014334, 21014335, 21014336, 21014337, 21014338, 21014339, 21014340, 21014341, 21014353]
# # 给主播修改公会信息
# for i in range(21):
#     for j in range(3):
#         # 修改主播所属公会
#         gh_uid = 100000001 + j + (i * 3)
#         myquery = {"_id": gh_uid, "star.broker": 1202363}
#         newvalues = {"$set": {"star.broker": a[i]}}
#         mydb.update_one(myquery, newvalues)
#
#         # 检查是否修改成功
#         # myclient = pymongo.MongoClient(host="192.168.31.229", port=26000)
#         # mydb = myclient["xy"]["users"]
#         # gh_uid = 100000001 + j + (i * 3)
#         # myc1 = mydb.find_one({"_id": gh_uid})
#         # print("%s--%s" % (myc1["star"]["broker"], j * i))
#


# 修改公会昵称
# a = [20883701,21014300,21014301,21014313,21014314,21014315,21014316,21014317,21014318,21014319,21014320,21014321,21014334,21014335,21014336,21014337,21014338,21014339,21014340,21014341,21014353]
# for i in range(21):
#     myclient = pymongo.MongoClient(host="192.168.31.229", port=26000)
#     mydb = myclient["xy"]["users"]
#     myc1 = mydb.find_one({"_id": a[i]})
#     b = myc1["nick_name"]
#     # print(myc1["nick_name"])
#     myquery = {"_id":a[i],"nick_name":b}
#     c = "公会000"
#     newvalues = {"$set": {"nick_name":(c + str(i+1))}}
#
#     mydb.update_one(myquery, newvalues)
#
#     myc1 = mydb.find_one({"_id": a[i]})
#     d = myc1["nick_name"]
#     print("%s---%s"%(i+1,d))


# a = [1,2]
# b = ["a","b","c","d","e","f"]
# for i in range(2):
#     for j in range(3):
#         print(str(a[i])+b[j+(i*3)])





# 以下是公会战脚本
# 删除mongdb的公会的所以信息
# myclient = pymongo.MongoClient(host="192.168.31.229", port=26000)
# mydb = myclient["xy_spark"]["broker_battle_team"]
# mydb.drop()


# 批量进行,公会的主播设置名称与公会添加主播
# 1、获取token
# a=[]
# for i in range(20):
#     ghid = "gh000" + str(i+1)
#     username = ghid
#     data_auth = {"username": username, "password": "123456", "grant_type": "password", "scope": "PC_WEB"}
#     url = "https://test-amber.memeyule.com/api/v1/oauth2/token"
#     ret = requests.post(url, data=data_auth)
#     access_token = ret.json()["access_token"]
#     a.append(access_token)
#     user_token = ("%s的token是%s")%(ghid,access_token)
#     print(user_token)
# print(a)
# #
#
# # # 2、设置战队名
# for i in range(20):
#     access_token1 = a[i]
#     url = "https://test-spark.memeyule.com/api/v1/years20/broker-battle/team-name?access_token="+access_token1
#     gh_name = "公会" + str(i + 1)
#     gh_data = {"name": gh_name}
#     ret = requests.post(url,data=json.dumps(gh_data))
#     name_zd = ("%s战队设置成功--%s") % (gh_name, i+1)
#     print(name_zd)
#
#
# # 3、添加主播（每个公会添加三个主播）
# time.sleep(5)
# for i in range(20):
#     for j in range(3):
#         access_token2 = a[i]
#         url = "https://test-spark.memeyule.com/api/v1/years20/broker-battle/add-member?access_token="+access_token2
#         # access_token = a[i]
#         gh_name = "公会000" + str(i + 1)
#         gh_uid = 100000001 + j+(i*3)
#         gh_data = {"uid": gh_uid}
#         ret = requests.post(url,data=json.dumps(gh_data))
#         name_zd = ("%s主播添加成功--%s") % (gh_uid, j+(i*3) )
#         print(name_zd)



#筛选阶段送礼
# username = "www56"
# data_auth = {"username": username, "password": "123456", "grant_type": "password", "scope": "PC_WEB"}
# url = "https://test-amber.memeyule.com/api/v1/oauth2/token"
# ret = requests.post(url, data=data_auth)
# user_token = ret.json()["access_token"]
# for i in range(100):
#     access_token = user_token
#     kt_id = str(100000001+i)
#     gift_id = "717"
#     gift_count =  str(i+1)
#     url = "https://test-api.memeyule.com/room/send_gift/"+access_token+"/"+kt_id+"/"+gift_id
#     gift_data={"count":gift_count,"user_id":kt_id,"marquee":"yes"}
#     requests.get(url,params=gift_data)
#     print("送%s--%s个礼物--%s"%(kt_id,gift_count,i+1))



# 公会长设置主播
# for i in range(21):
#     for j in range(3):
#         access_token2 = a[i]
#         url = "https://test-spark.memeyule.com/api/v1/years20/broker-battle/pk-member?access_token="+access_token2
#         # access_token = a[i]
#         gh_name = "公会000" + str(i + 1)
#         gh_uid = 100000001 + j+(i*3)
#         gh_data = {"uid": gh_uid}
#         ret = requests.post(url,data=json.dumps(gh_data))
#         name_zd = ("%s主播设置成功--%s") % (gh_uid, j+(i*3) )
#         print(name_zd)

# 多人房送礼
# url = "https://test-api.memeyule.com/multireceiver/send_gift.json"
# gift_data = {"star_list":star_id,"marquee":"yes","gift_id":gift_id,"count":count,"stage_room_id":stage_room_id,"multi_type":"multi_pk","companion_room_id":stage_room_id,"access_token":access_token}
# requests.get(url,params=gift_data)


# token1 = "2020-11-30 14:59:32.000000"
# # datetime.datetime.now()>(token.created + timedelta(days=settings.TOKEN_LIFETIME))
# print(datetime.datetime.now())
# print(type(datetime.datetime.now()))
# days=settings.TOKEN_LIFETIME
# print(days)
# print(type(days))

# print(datetime.datetime.timestamp(datetime.datetime.now()))
# token ="1606728021.0932462yh01"
# token_obj=models.userToken.objects.filter(token=token).first()
# print(token_obj)
# if datetime.datetime.timestamp(datetime.datetime.now()) > (datetime.datetime.timestamp(token_obj.update_time) + settings.TOKEN_LIFETIME):
#     print(datetime.datetime.timestamp(datetime.datetime.now()))
#     print(datetime.datetime.timestamp(token_obj.update_time))
#     print(settings.TOKEN_LIFETIME)
#     print((datetime.datetime.timestamp(token_obj.update_time) + settings.TOKEN_LIFETIME))
#     print("token失效")
#     token_obj.delete()
#     print(token_obj)
# else:
#     print(datetime.datetime.timestamp(datetime.datetime.now()))
#     print(datetime.datetime.timestamp(token_obj.update_time))
#     print(settings.TOKEN_LIFETIME)
#     print((datetime.datetime.timestamp(token_obj.update_time) + settings.TOKEN_LIFETIME))
#     print("token未失效")
# a={"a":1,"b":1,"c":1,}
# print(a.keys())
# print(type(a.keys()))
# print(list(a.keys()))
# print(type(list(a.keys())))


# myclient = pymongo.MongoClient(host="192.168.31.229", port=26000)
# mydb = myclient["xy"]["users"]
# myc1 = mydb.find_one({"_id": 1492303})


# 查询主播token
# myclient = pymongo.MongoClient(host="192.168.31.229",port=10000)
# mydb = myclient["xy_user"]["users"]
# myc1 =mydb.find_one({"mm_no": "100000010"})
# print(myc1["token"])

# 修改主播的开播状态
# myclient = pymongo.MongoClient(host="192.168.31.229",port=26000)
# mydb = myclient["xy"]["rooms"]
# myquery = {"_id":1492247}
# newvalues = {"$set": {"live":True}}
# mydb.update_one(myquery, newvalues)


# def fun1():
#     print(1)
# print(fun1.__name__)
# print(fun1)
#
# sum =lambda a,b :a+b
# print(sum(1,2))
# a= "a,b,c"
# print(a.split(","))
# print(type(a.split(",")))
# print("".join(a.split(",")))
# print(type(":".join(a.split(","))))
a=dict((("one","1"),("two","1"),("three","1")))
dict((('one', 1),('two', 2),('three', 3)))
print(a)