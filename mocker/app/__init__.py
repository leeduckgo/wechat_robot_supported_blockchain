# -*- coding: utf-8 -*-
from flask import Flask

from . import views

# 初始化flask应用
app = Flask(__name__)

# 初始化数据库
