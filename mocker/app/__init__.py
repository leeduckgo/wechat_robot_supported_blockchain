#-*- coding:utf-8 -*-


from flask import Flask


# 初始化flask应用
app = Flask(__name__)

# 初始化数据库

from app import views