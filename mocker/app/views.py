# -*- coding:utf-8 -*-


from flask import (
    request, make_response)
from . import app
import json
from functools import wraps

# ===cross_domain====
'''这个是允许跨域的代码'''


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst

    return wrapper_fun


# ===    end     ===

# ======index.html=======
'''这里是index中用到的API接口'''

'''indx_svg_list：获取gv列表'''


@app.route('/', methods=['GET', 'POST'])
@allow_cross_domain
def index_get_command():
    print("body:")
    print(trans(request.get_data()))  # body

    print("headers:")
    print(request.headers)  # header

    print("args:")
    print(request.args)  # args

    return json.dumps({"result": "success"})


# ===    end     ===

'''pretty json '''


def trans(payload):
    try:
        a_json = json.loads(str(payload, "utf-8"))
        return json.dumps(a_json, sort_keys=True, indent=4, separators=(',', ':'))
    finally:
        print("not json")
        return payload

# '''Python => front'''
# def msg_traslate_to_front(msg_all):
#     try:
#         msg_after_trans={msg_all[0].class_name:[]}
#
#         for every_msg in msg_all:
#             a_msg={}
#
#             for every_vary in every_msg.class_varies:
#                 a_msg[every_vary]=every_msg.get_vary(every_vary)
#
#             msg_after_trans[msg_all[0].class_name].append(a_msg)
#         print(json.dumps(msg_after_trans))
#         #data format:{posts:[{a:b,c:d},{a:e,c:f}...]}
#         return json.dumps(msg_after_trans)
#     except:
#         return None

# '''front => python'''
# def msg_translate_from_front(request):
#     msg_data_old=request.form.to_dict()
#     for i in msg_data_old:
#         msg_data_new= json.loads(i)
#     print(msg_data_new)
#     return msg_data_new

# ===    end     ===
