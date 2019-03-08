from random import choice
from settings import PROJECT_PATH, GTOUP1
import os

class Replier():
    def __init__(self, bot, list_dir, logger):
        self.bot = bot
        self.group = self.bot.groups().search(GTOUP1)[0]
        self.log = logger
        self.list_dir = list_dir


    def random_img(self):
        """随机获取图片"""
        path = choice(self.list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join(PROJECT_PATH, "pics", path)

    def handle_msg(self, msg):
        self.log.info(msg)
        if str.find(msg.text, "随机超越") != -1:
            path = self.random_img()
            self.group.send_image(path)
        if str.find(msg.text, "燃烧") != -1:
            return "燃烧我的卡路里！"

