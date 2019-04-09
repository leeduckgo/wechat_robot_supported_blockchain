# -*- coding: utf-8 -*-
from time import sleep

from wxpy import Bot
from wxpy import embed
from wxpy import Group

from common.logger import Logger
from common.message_replier import Replier

# === init ===
# user.name 用户群内备注名称
# user.nick_name 用户微信名称
bot = Bot(console_qr=True)  # 控制台二维码
#bot = Bot(cache_path=True)  # 短时间内重启无需重新登录
bot.enable_puid()
logger = Logger()  # 项目logger对象
replier = Replier(bot)


# === main process ===
if __name__ == '__main__':
    @bot.register()
    def reply_message(msg):
        # logger.info(msg.sender)
        """消息回复"""
        if type(msg.sender) == Group:  # 所有群组消息
            if msg.sender.puid in ["20ed458a", "dc8c27cb"]:  # 限定群组
                logger.info("=== start ===")
                replier.set_group(msg.sender.puid) # 获取群信息
                logger.info(msg.member.puid)
                if msg.type == "Note":
                    replier.update_user_info(msg)
                typ, content1, content2 = replier.handle_group_msg(msg)
                if typ == 'text':
                    msg.reply_msg(content1)
                elif typ == 'img':
                    msg.reply_image(content1)
                elif typ == 'both':
                    # msg.reply_image(content1)
                    msg.sender.send_image(content1)
                    sleep(1)
                    msg.reply_msg(content2)
        # else:  # todo 私聊消息
        #     replier.handle_solo_msg(msg)
        #     logger.info(msg)

    embed()  # 阻塞线程不退出'
