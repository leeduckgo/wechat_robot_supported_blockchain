from random import choice
from wxpy import Bot
import os
from common.logger import Logger
from settings import PROJECT_PATH, GTOUP1

bot = Bot()
group = bot.groups().search(GTOUP1)[0]
log = Logger()
list_dir = os.listdir(os.path.join(PROJECT_PATH, 'pics'))


def random_img():
    """随机获取图片"""
    global list_dir
    path = choice(list_dir)
    log.info('choose:-->{}'.format(path))
    return os.path.join(PROJECT_PATH, "pics/", path)


@bot.register(group)
def reply_group(msg):
    """群组消息回复"""
    global group
    log.info(msg)
    if str.find(msg.text, "随机超越") != -1:
        path = random_img()
        group.send_image(path)
