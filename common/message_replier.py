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
        self.rsp_game_player_map = {}

    def set_group(self, puid):
        self.group.set_group(puid)
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
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] != "本群简介":
            return empty_result
        d = get_group_introduction(msg.member.group.puid)
        if not d:
            return empty_result
        return 'text', d.get('introduction'), ''

    def finger_guessing_game(self, msg):
        """
        猜拳游戏
        :param msg:
        :return:
        """
        group_id = msg.member.group.puid  # 群组唯一id
        name = msg.member.display_name  # 玩家名
        id = msg.member.puid  # 玩家id
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "石头剪刀布" or real_msg[len(real_msg) - 1] == "剪刀石头布" \
                or real_msg[len(real_msg) - 1] == "猜拳":
            if group_id not in self.rsp_game_player_map.keys():  # 如果字典中不存在该群组id,构建字典
                # { 群组id : {玩家id: [游戏对象 , 开始游戏的时间, 玩家名]}}
                self.rsp_game_player_map.update(
                    {
                        group_id: {
                            id: [RspGame(5), now_to_datetime4(), name]
                        }
                    }
                )
            elif group_id in self.rsp_game_player_map.keys() and \
                    id not in self.rsp_game_player_map.get(group_id, {}).keys():  # 每个群只能同时运行一个游戏避免混乱
                return 'text', '@' + msg.member.display_name + \
                       " 有玩家在玩哟,稍等一下",''
            self.rsp_game_player_map[group_id][id][0].start(name)  # 开始游戏
            return 'text', '@' + msg.member.display_name + \
                   " 石头剪刀布开始，你先出吧，赢了我有奖励哦(五局三胜)", ''
        return empty_result

    def play_game(self, msg):
        """
        游戏
        :param msg:
        :return:
        """
        group_id = msg.member.group.puid
        name = msg.member.display_name
        id = msg.member.puid
        player_map = self.rsp_game_player_map
        # 如果字典中包含群组id并且 玩家id在字典中
        if player_map.get(group_id) and id in player_map.get(group_id, {}).keys():
            is_overtime = now_to_datetime4() > five_minutes_later(player_map[id][1])
            if is_overtime:
                msg = '@' + name + ' 游戏已经超时自动终止了呀!'
                msg.chat.send_msg(msg)
                player_map.pop(group_id)  # 超时删除群组id对应的字典

        if player_map.get(group_id):
            if id not in player_map.get(group_id, {}).keys():  # 不是玩家的消息，不进行回应
                return 'text', '@' + msg.member.display_name + " 先等等哦，我正在跟@" + \
                       player_map[id][2] + " 玩石头剪刀布", ''
            else:
                cancel, result, pic = player_map[id][0].play(msg)  # 玩游戏
                self.log.debug('game result:{} pic:{}'.format(result, pic))
                if cancel == 1:
                    player_map.pop(group_id)  # 如果游戏结束, 删除群组id对应的字典
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
        if msg.text in ("杨超越", "天降超越"):  # todo 待增加
            path = self.random_img()
            self.log.debug(path)
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
