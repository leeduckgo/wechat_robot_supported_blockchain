# -*- coding: utf-8 -*-

from wxpy import embed
from wxpy import Bot
from wxpy import User
from wxpy import Group
from common.message_replier import Replier  # 导入即运行
from common.logger import Logger
from time import sleep
import secret

# === init ===
# user.name 用户群内备注名称
# user.nick_name 用户微信名称
# bot = Bot(cache_path=True, console_qr=True)  # 控制台二维码
#bot = Bot(cache_path=True)  # 短时间内重启无需重新登录
bot = Bot()
bot.enable_puid()
logger = Logger()  # 单例模式下项目中只会创建一个logger对象

# === main process ===
if __name__ == '__main__':
    replier = Replier(secret.api_key)
    # 自动接受新的好友请求
    def reply_solo(msg):
        """接受好友请求"""
        friend = msg.sender
        # 向新的好友发送消息
        friend.send('你好呀,我是全村的希望!')  # todo 内容待定 附加功能介绍
        friend.send('参与内测请扫码加群：')
        friend.send_image('group.jpeg')
    
    @bot.register()
    def reply_message(msg):
        print(msg.sender)
        """消息回复"""
        if type(msg.sender) == Group:  # 所有群组消息
            if msg.sender.puid in ["1f423133", "4193b4db"]: #限定群组
                print("=== start ===")
                replier.set_group(msg.sender.puid) # 获取群信息
                print(msg.member.puid)  
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
            reply_solo(msg)
            logger.info(msg)

    embed()  # 阻塞线程不退出'
