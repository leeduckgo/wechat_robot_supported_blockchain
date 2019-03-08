from random import choice
from settings import PROJECT_PATH
import os

class Replier():
    def __init__(self, bot, group, list_dir, logger):
        self.bot = bot
        self.group = group
        self.log = logger
        self.list_dir = list_dir


    def random_img(self):
        """随机获取图片"""
        path = choice(self.list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join("pics", path)

    def handle_msg(self, msg, tuling):
        self.log.info(msg)
        if str.find(msg.text, "随机超越") != -1:
            path = self.random_img()
            print(path)
            self.group.send_image(path)
        if str.find(msg.text, "燃烧") != -1:
            self.group.send("燃烧我的卡路里！")
        if not msg.is_at:#如果没有@到机器人，不进行回应
            return
        else:
            tuling.do_reply(msg)#@到机器人，则用图灵机器人进行回应


