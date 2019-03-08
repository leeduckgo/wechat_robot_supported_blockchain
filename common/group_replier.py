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

    def handle_msg(self, msg):
        if str.find(msg.text, "随机超越") != -1:
            self.log.info(msg)
            path = self.random_img()
            print(path)
            self.group.send_image(path)
        
        # if str.find(msg.text, "燃烧") != -1:
        #     return "燃烧我的卡路里！"

