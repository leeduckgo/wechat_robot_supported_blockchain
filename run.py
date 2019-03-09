# -*- coding: utf-8 -*-
from wxpy import embed,Bot,Tuling
from common.group_replier import Replier # 导入即运行
from common.group_manager import Manager
from common.ycy_replier import YcyReplier
import os
from common.logger import Logger
from settings import PROJECT_PATH, GROUP1

# === init ===

bot = Bot()
bot.enable_puid()
group = bot.groups().search(GROUP1)[0]
list_dir = os.listdir(os.path.join('resources', 'pics'))
logger = Logger()
tuling=Tuling(api_key='e889671fd22348528747941d7e563e02')
manager = Manager(group)

# === manager operation ===

members = manager.all_members()
logger.info(members)
ycy_replier = YcyReplier()
replier = Replier(bot, group, list_dir, logger, ycy_replier)
# === main process ===
@bot.register(group)
def reply_group(msg):
    logger.info(msg)
    """群组消息回复""" 
    replier.handle_msg(msg, tuling)


embed()  # 阻塞线程不退出'
