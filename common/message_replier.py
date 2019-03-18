# -*- coding: utf-8 -*-
import os
import re
from random import choice
from wxpy import Tuling
from common.logger import Logger
from common.ycy_replier import YcyReplier
from common.rock_scissors_paper import RspGame
from common.communication import create_messages
from common.communication import get_group_introduction
from settings import TULING_KEY
from datetime import datetime
from utils.utils import now_to_datetime4
from utils.utils import five_minutes_later

empty_result = ('', '', '')


class Replier(object):
    """消息回复"""

    def __init__(self):
        # self.group = group
        self.log = Logger()
        self.ycy = YcyReplier()
        self.tuling = Tuling(api_key=TULING_KEY)
        self.rsp_game = RspGame(5)
        self.rsp_game_player_name = ''
        self.rsp_game_flag = False  # 是否开启石头剪刀布游戏
        self.start_game_time = None  # 游戏开始时间

    def random_img(self):
        """
        随机获取图片
        :return:
        """
        list_dir = os.listdir(os.path.join('resources', 'pics'))
        path = choice(list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join("resources", "pics", path)

    def handle_leave_message(self, msg):
        """
        处理留言
        :param msg:
        :return:
        """
        is_leave_message = re.search(r'(留言:|留言：)(.*)', msg.text)
        if is_leave_message:
            content = is_leave_message.group(2).strip()  # 获取第二组内容并去除前后空格
            self.log.info('留言内容:{}'.format(content))
            status = create_messages(name=msg.member.name, content=content, fans_id=msg.member.puid)
            if status == 200:
                return 'text', '@' + msg.member.display_name + ' ' + "留言成功！点击 {} 可查看你的留言".format(
                    'http://ycy.ahasmarter.com/'
                ), ''
            else:
                return 'text', '@' + msg.member.display_name + ' ' + "留言失败！稍后再尝试吧", ''
        return empty_result

    def get_group_introduction(self, msg):
        """
        获取群介绍
        :param msg:
        :return:
        """
        is_get_group_introduction = re.findall(r'本群简介', msg.text)
        if not is_get_group_introduction:
            return empty_result
        d = get_group_introduction(msg.sender.group.puid)
        if not d:
            return empty_result
        return 'text', d.get('introduction'), ''

    def finger_guessing_game(self, msg):
        """
        猜拳游戏
        :param msg:
        :return:
        """
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "石头剪刀布" or real_msg[len(real_msg) - 1] == "剪刀石头布" \
                or real_msg[len(real_msg) - 1] == "猜拳":
            self.rsp_game_player_name = msg.member.display_name
            self.rsp_game.start(msg.member.display_name)
            self.start_game_time = datetime.now()
            self.rsp_game_flag = True
            return 'text', '@' + msg.member.display_name + \
                   " 石头剪刀布开始，你先出吧，赢了我有奖励哦(五局三胜)", ''
        return empty_result

    def play_game(self, msg):
        """
        游戏
        :param msg:
        :return:
        """
        if self.rsp_game_flag:
            # 游戏超过5分钟未结束,强制终止,避免用户长时间占用机器人
            if now_to_datetime4() > five_minutes_later(self.start_game_time):
                self.rsp_game_flag = False
                self.start_game_time = None
                self.rsp_game_player_name = ''
                return '', '', ''
            if self.rsp_game_player_name != msg.member.display_name:  # 不是玩家的消息，不进行回应
                return 'text', '@' + msg.member.display_name + " 先等等哦，我正在跟@" + \
                       self.rsp_game_player_name + " 玩石头剪刀布", ''
            else:
                cancel, result, pic = self.rsp_game.play(msg)
                self.log.debug('game result:{} pic:{}'.format(result, pic))
                if cancel == 1:
                    self.rsp_game_flag = False
                return 'both', pic, result
        typ, content1, content2 = self.finger_guessing_game(msg)  # 猜拳游戏
        if typ == 'text':
            return typ, content1, content2
        return empty_result

    def handle_msg(self, msg):
        """
        处理回复消息
        :param msg:
        :return:
        """
        self.log.info('receive: %s' % msg.text)
        if msg.text in ("杨超越",):  # todo 待增加
            path = self.random_img()
            self.log.debug(path)
            # self.group.send_image(path)
            return 'img', path, ''

        real_msg = msg.text.split()
        respond_msg = self.ycy.reply_text(real_msg[len(real_msg) - 1])  # 超越语录无需要@
        if respond_msg:
            return 'text', '@' + msg.member.display_name + ' ' + respond_msg, ''

        if msg.is_at:  # 如果@到机器人，进行的回应
            typ, content1, content2 = self.play_game(msg)  # 玩游戏,高优先级,内部存在拦截其他回复
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            typ, content1, content2 = self.handle_leave_message(msg)  # 处理留言请求
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            typ, content1, content2 = self.get_group_introduction(msg)  # 处理留言请求
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            self.log.info(self.tuling.reply_text(msg).replace("图灵机器人", "超越宝宝"))
            return 'text', self.tuling.reply_text(msg).replace("图灵机器人", "超越宝宝"), ''

        return empty_result
