from random import choice
from settings import PROJECT_PATH
import os


class Replier(object):
    def __init__(self, bot, group, list_dir, logger, ycy, tuling):
        self.bot = bot
        self.group = group
        self.log = logger
        self.list_dir = list_dir
        self.ycy = ycy
        self.tuling = tuling

    def random_img(self):
        """随机获取图片"""
        path = choice(self.list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join("resources","pics", path)

    def handle_msg(self, msg):
        self.log.info(msg)
        if msg.text == "天降超越":
            path = self.random_img()
            print(path)
            self.group.send_image(path)
            return
        if str.find(msg.text, "燃烧") != -1:
            self.group.send("燃烧我的卡路里！")  
            return 
        if not msg.is_at:#如果没有@到机器人，不进行回应
            return
        else:
            real_msg = msg.text.split()
            self.log.debug("send： "+real_msg[len(real_msg)-1])
            respond_msg = self.ycy.reply_text(real_msg[len(real_msg)-1])        
            if respond_msg :
                self.group.send('@' + msg.member.display_name + ' ' + respond_msg)
            else:
                self.group.send(self.tuling.reply_text(msg).replace("图灵机器人","超越宝宝"))#@到机器人，则用图灵机器人进行回应

