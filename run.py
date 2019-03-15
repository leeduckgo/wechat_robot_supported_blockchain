# -*- coding: utf-8 -*-

from wxpy import embed
from wxpy import Bot
from wxpy import User
from wxpy import Group
from common.message_replier import Replier  # 导入即运行
from common.logger import Logger

# === init ===

# bot = Bot(cache_path=True, console_qr=True)  # 控制台二维码
bot = Bot(cache_path=True)  # 短时间内重启无需重新登录
bot.enable_puid()
logger = Logger()  # 单例模式下项目中只会创建一个logger对象

# === main process ===
if __name__ == '__main__':

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
            replier = Replier()
            typ, content = replier.handle_msg(msg)
            if typ == 'text':
                msg.reply(content)
            elif typ == 'img':
                msg.reply_image(content)
        else:  # todo 私聊消息
            logger.info(msg)

    embed()  # 阻塞线程不退出'
