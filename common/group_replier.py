from random import choice
from settings import PROJECT_PATH
import os
import jieba
import jieba.analyse

class Replier(object):
    def __init__(self, bot, group, list_dir, logger, ycy, tuling, rsp_game):
        self.bot = bot
        self.group = group
        self.log = logger
        self.list_dir = list_dir
        self.ycy = ycy
        self.tuling = tuling
        self.rsp_game_flag = False #是否开启石头剪刀布游戏
        self.rsp_game = rsp_game
        self.rsp_game_player_name = ''

    def random_img(self):
        """随机获取图片"""
        path = choice(self.list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join("resources","pics", path)

    def handle_msg(self, msg):
        self.log.info(msg)
        '''进行石头剪刀布游戏'''
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
            self.log.debug("send:"+real_msg[len(real_msg)-1])
            if real_msg[len(real_msg)-1] == "石头剪刀布":   
                self.rsp_game_flag = True
                self.rsp_game_player_name = msg.member.display_name
                self.rsp_game.start(msg.member.display_name)
                self.group.send('@' + msg.member.display_name + " 石头剪刀布开始，你先出吧，赢了我有奖励哦(五局三胜)")
                return
            respond_msg = self.ycy.reply_text(real_msg[len(real_msg)-1])        
            if respond_msg :
                self.group.send('@' + msg.member.display_name + ' ' + respond_msg)
            else:
                self.group.send(self.tuling.reply_text(msg).replace("图灵机器人","超越宝宝"))#@到机器人，则用图灵机器人进行回应

