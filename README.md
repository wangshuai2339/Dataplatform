# Dataplatform 平台（测试数据、测试脚本、接口自动化、PC自动化、App自动化、持续集成）

## 项目结构

```
meme
├── meme                 #系统自动生成的配置
    ├── settings.py      #系统配置
    ├── urls.py	         #url路径配置
├── memetest
    ├── admin.py	     #django自带的admin平台
    ├── models.py        #模型
    ├── serializers.py	 #模型序列化
    ├── tests.py         #测试
    ├── views.py         #视图函数
├── migrations           #数据更新记录
├── static               #前端文件，前后端不分离时使用。本平台前后端分离，所以用不到
├── templates            #前端html文件，前后端不分离时使用。本平台前后端分离，所以用不到
```