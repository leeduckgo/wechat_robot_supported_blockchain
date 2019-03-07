# -*- coding: utf-8 -*-
from random import choice
from wxpy import *
bot = Bot()
group = bot.groups().search('超越微信机器人')[0]

@bot.register(group)
def reply_group(msg):
    global group
    print(msg)
    if str.find(msg.text, "随机超越") != -1:
        group.send_image("pics/ycy.png")

embed() #阻塞线程不退出
