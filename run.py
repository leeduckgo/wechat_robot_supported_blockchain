# -*- coding: utf-8 -*-
from wxpy import embed,Bot
from common.group_replier import Replier # 导入即运行
import os
from common.logger import Logger
from settings import PROJECT_PATH, GTOUP1

# === init ===

bot = Bot()
bot.enable_puid()
group = bot.groups().search(GTOUP1)[0]
list_dir = os.listdir(os.path.join(PROJECT_PATH, 'pics'))
logger = Logger()

# === main process ===
@bot.register(group)
def reply_group(msg):
    """群组消息回复"""
    replier = Replier(bot, group, list_dir, logger)
    replier.handle_msg(msg)

embed()  # 阻塞线程不退出
