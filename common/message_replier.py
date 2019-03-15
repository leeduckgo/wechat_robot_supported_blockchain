from random import choice
import os
from wxpy import Tuling
from common.logger import Logger
from common.ycy_replier import YcyReplier
from common.rock_scissors_paper import RspGame
from settings import TULING_KEY


class Replier(object):
    """消息回复"""

    def __init__(self):
        # self.group = group
        self.log = Logger()
        self.ycy = YcyReplier()
        self.tuling = Tuling(api_key=TULING_KEY)
        self.rsp_game_flag = False #是否开启石头剪刀布游戏
        self.rsp_game = RspGame(5)
        self.rsp_game_player_name = ''

    def random_img(self):
        """随机获取图片"""
        list_dir = os.listdir(os.path.join('resources', 'pics'))
        path = choice(list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join("resources", "pics", path)

    def handle_msg(self, msg):
        """进行游戏"""
        if self.rsp_game_flag:
            if not msg.is_at:#如果没有@到机器人，不进行回应
                return
            elif self.rsp_game_player_name != msg.member.display_name:#不是玩家的消息，不进行回应
                self.group.send('@' + msg.member.display_name + " 先等等哦，我正在跟@" + self.rsp_game_player_name+ " 玩石头剪刀布")  
                return 
            else:
                cancel, result, pic = self.rsp_game.play(msg)
                if cancel == 1:
                    self.rsp_game_flag = False
                    self.group.send_image(pic)
                    self.group.send(result)
                else:
                    self.group.send_image(pic)
                    self.group.send(result)
                return

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
        if not msg.is_at:  # 如果没有@到机器人，不进行回应
            return '', ''
        else:
            real_msg = msg.text.split()
            self.log.debug("send:"+real_msg[len(real_msg)-1])
            if real_msg[len(real_msg)-1] == "石头剪刀布":   
                self.rsp_game_flag = True
                self.rsp_game_player_name = msg.member.display_name
                self.rsp_game.start(msg.member.display_name)
                self.group.send('@' + msg.member.display_name + " 石头剪刀布开始，你先出吧，赢了我有奖励哦(五局三胜)")
                return
            respond_msg = self.ycy.reply_text(real_msg[len(real_msg) - 1])
            if respond_msg:
                return 'text', '@' + msg.member.display_name + ' ' + respond_msg
            else:
                return 'text', self.tuling.reply_text(msg).replace("图灵机器人", "超越宝宝")
