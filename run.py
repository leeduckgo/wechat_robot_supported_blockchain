# -*- coding: utf-8 -*-
import traceback
from time import sleep
from wxpy import embed
from wxpy import Bot
from wxpy import Group
from wxpy import ensure_one
from wxpy import get_wechat_logger
from common.message_replier import Replier
from common.logger import Logger

# === init ===

# bot = Bot(cache_path=True, console_qr=True)  # 控制台二维码
bot = Bot(cache_path=True)  # 短时间内重启无需重新登录
bot.enable_puid()
log = Logger()  # 项目logger对象
replier = Replier()


# === main process ===
if __name__ == '__main__':
    try:
        # 自动接受新的好友请求
        @bot.register(msg_types='Friends')
        def auto_accept_friends(msg):
            """接受好友请求"""
            new_friend = msg.card.accept()
            # 向新的好友发送消息
            new_friend.send('你好呀,我是全村的希望!')  # todo 内容待定 附加功能介绍

        @bot.register()
        def reply_message(msg):
            """消息回复"""
            if type(msg.sender) == Group:  # 所有群组消息
                typ, content1, content2 = replier.handle_msg(msg)
                if typ == 'text':
                    msg.reply_msg(content1)
                elif typ == 'img':
                    msg.reply_image(content1)
                elif typ == 'both':
                    msg.reply_image(content1)
                    sleep(1)
                    msg.reply_msg(content2)
            else:  # todo 私聊消息
                log.info(msg.text)
    except Exception:
        # 找到需要接收日志的群 -- `ensure_one()` 用于确保找到的结果是唯一的，避免发错地方
        group_receiver = ensure_one(bot.groups().search('超越微信机器人'))
        logger = get_wechat_logger(group_receiver)  # 重大错误监控,发送消息至指定群聊
        logger.error(traceback.format_exc())

    embed()  # 阻塞线程不退出'
