# -*- coding: utf-8 -*-
import os
import random

from random import choice

from common.logger import Logger


class RspGame(object):
    """
    随机整数[1,3]决定机器人出招，分别为1：石头；2:剪刀；3：布
    """

    def __init__(self, game_num):
        self.log = Logger()
        self.game_all_num = game_num
        self.player_score = 0
        self.com_score = 0
        self.player_name = ''
        self.img_dir = ['rock', 'scissors', 'paper', 'emoticon']
        # self.rsp_img = [os.path.join(GAME_IMAGE_PATH, 'rock_1.jpg'), os.path.join(GAME_IMAGE_PATH, 'scissors_1.jpg'), os.path.join(GAME_IMAGE_PATH, 'paper_1.jpg')]
        # print(self.rsp_img)
        self.draw_msg = " 平局了，继续来~"
        self.fail_msg = " 我输了 "
        self.win_msg = " 我赢了 "
        self.over_msg = [" 游戏结束，你输了", " 游戏结束，恭喜你赢了"]
        self.msg_code = {"石头": 0, "剪刀": 1, "布": 2}

    def start(self, player_name):
        self.player_score = 0
        self.com_score = 0
        self.player_name = player_name

    def random_img(self, random_num):
        list_dir = os.listdir(os.path.join('resources', 'game', self.img_dir[random_num]))
        path = choice(list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join('resources', 'game', self.img_dir[random_num], path)

    def get_result(self, winer):
        """获取本场比赛情况"""
        if winer == 1:
            self.player_score += 1
            if self.player_score == (self.game_all_num + 1) / 2:
                return 1, '@' + self.player_name + self.over_msg[1]
            else:
                return 0, '@' + self.player_name + self.fail_msg
        elif winer == -1:
            self.com_score += 1
            if self.com_score == (self.game_all_num + 1) / 2:
                return 1, '@' + self.player_name + self.over_msg[0]
            else:
                return 0, '@' + self.player_name + self.win_msg

    def play(self, msg):
        """
        返回[a, b, c]
        a代表游戏是否已经结束 1:结束 0:未结束
        b代表本次出招结果
        c代表本次出招图片
        :param msg:
        :return:
        """
        self.log.info('play:{}'.format(msg))
        real_msg = msg.text.split()
        valid_msg = real_msg[len(real_msg) - 1]
        self.log.debug('commond:{}'.format(valid_msg))
        if str.find(valid_msg, "不玩") != -1 or str.find(valid_msg, "退出") != -1:
            return 1, '@' + self.player_name + " 虽然半途而废不怎么好听，但有时候放弃也是一种聪明的选择", self.random_img(3)
        elif valid_msg != "石头" and valid_msg != "剪刀" and valid_msg != "布":
            return 0, '@' + self.player_name + " 不遵守游戏规则，会被我拉人黑名单", self.random_img(3)
        random_num = random.randint(1, 3) - 1
        self.log.debug('random_num:{}'.format(random_num))
        self.log.debug('msg_code:{}'.format(self.msg_code[valid_msg]))
        # 1：玩家 -1：机器人 0：平局
        winer = (random_num - self.msg_code[valid_msg] + 4) % 3 - 1
        if winer == 0:
            return 0, '@' + self.player_name + self.draw_msg, self.random_img(random_num)
        else:
            can, res_msg = self.get_result(winer)
            return can, res_msg, self.random_img(random_num)
