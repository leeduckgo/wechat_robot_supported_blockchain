from random import choice
import os
from wxpy import Tuling
from common.logger import Logger
from common.ycy_replier import YcyReplier
from settings import TULING_KEY
import re
from common.communication import create_messages


class Replier(object):
    """回复消息"""

    def __init__(self):
        # self.group = group
        self.log = Logger()
        self.ycy = YcyReplier()
        self.tuling = Tuling(api_key=TULING_KEY)

    def random_img(self):
        """随机获取图片"""
        list_dir = os.listdir(os.path.join('resources', 'pics'))
        path = choice(list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join("resources", "pics", path)

    def handle_leave_message(self, msg):
        """处理留言"""
        is_leave_message = re.search(r'(留言:|留言：)(.*)', msg.text)
        if is_leave_message:
            content = is_leave_message.group(2).strip()  # 获取第二组内容并去除前后空格
            self.log.info('留言内容:{}'.format(content))
            status = create_messages(name=msg.member.name, content=content, fans_id=msg.member.puid)
            if status == 200:
                return 'text', '@' + msg.member.name + ' ' + "留言成功！点击 {} 可查看你的留言".format(
                    'http://ycy.ahasmarter.com/'
                )
            else:
                return 'text', '@' + msg.member.name + ' ' + "留言失败！稍后再尝试吧"
        return '', ''

    def handle_msg(self, msg):
        """处理回复消息"""
        self.log.info(msg)

        if msg.text == "天降超越":
            path = self.random_img()
            self.log.debug(path)
            # self.group.send_image(path)
            return 'img', path
        if str.find(msg.text, "燃烧") != -1:
            # self.group.send()
            return 'text', "燃烧我的卡路里！"

        if msg.is_at:  # 如果没有@到机器人，不进行回应
            typ, content = self.handle_leave_message(msg)  # 处理留言请求
            if typ:
                self.log.info(content)
                return typ, content
            real_msg = msg.text.split()
            self.log.debug("send： " + real_msg[len(real_msg) - 1])
            respond_msg = self.ycy.reply_text(real_msg[len(real_msg) - 1])
            if respond_msg:
                return 'text', '@' + msg.member.name + ' ' + respond_msg
            else:
                return 'text', self.tuling.reply_text(msg).replace("图灵机器人", "超越宝宝")

        return '', ''
