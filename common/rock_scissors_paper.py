#1.增加不玩了退出功能 2.增加游戏计时退出功能 3.改成四种方式触发，超越猜拳、村花猜拳、剪刀石头布、石头剪刀布 4.玩游戏吧，列出已有的游戏列表
import random
from settings import GAME_IMAGE_PATH

#随机整数[1,3]决定机器人出招，分别为1：石头；2:剪刀；3：布
class RspGame(object):
    def __init__(self, logger, game_num):
        self.log = logger
        self.game_all_num = game_num
        self.player_score = 0
        self.com_score = 0
        self.player_name = ''
        self.rsp_img = [GAME_IMAGE_PATH + "\\rock_1.jpg", GAME_IMAGE_PATH + "\\scissors_1.jpg", GAME_IMAGE_PATH + "\\paper_1.jpg"]
        self.shadiao_img = GAME_IMAGE_PATH + "shadiao_today.gif"
        self.log.info("GAME_IMAGE_PATH:{}".format(self.rsp_img))
        self.draw_msg = " 平局了，继续来~"
        self.fail_msg = " 我输了 "
        self.win_msg =  " 我赢了 "
        self.over_msg = [" 游戏结束，你输了", " 游戏结束，恭喜你赢了"]
        self.msg_code = {"石头":0, "剪刀":1, "布":2}

    def start(self, player_name):
        self.player_score = 0
        self.com_score = 0
        self.player_name = player_name
        self.game_current_name = 0
        self.fail_msg = "@" + player_name + self.fail_msg
        self.win_msg = "@" + player_name + self.win_msg
        self.draw_msg = "@" + player_name + self.draw_msg
        self.over_msg[0] = "@" + player_name + self.over_msg[0]
        self.over_msg[1] = "@" + player_name + self.over_msg[1]

    '''获取本场比赛情况'''
    def get_result(self, winer):     
        if winer == 1:
            self.player_score += 1
            if self.player_score  == (self.game_all_num +1)/2:
                return 1, self.over_msg[1] + " 总比分：{}".format(self.com_score) + "-{}".format(self.player_score)
            else:
                return 0, self.fail_msg + " 目前比分：{}".format(self.com_score) + "-{}".format(self.player_score)
        elif winer == -1:
            self.com_score += 1
            if self.com_score == (self.game_all_num +1)/2:
                return 1, self.over_msg[0] + " 总比分：{}".format(self.com_score) + "-{}".format(self.player_score)
            else:
                return 0, self.win_msg + " 目前比分：{}".format(self.com_score) + "-{}".format(self.player_score)
            

    '''返回[a, b, c]'''
    '''a代表游戏是否已经结束 1:结束 0:未结束'''
    '''b代表本次出招结果'''
    '''c代表本次出招图片'''
    def play(self, msg):
        real_msg = msg.text.split()
        valid_msg = real_msg[len(real_msg)-1]
        self.log.debug('commond:{}'.format(valid_msg))
        if valid_msg != "石头" and valid_msg != "剪刀" and valid_msg != "布":
            return 0, '@' + self.player_name + " 你出的是错的！这叫我怎么出...", self.shadiao_img
        elif str.find(valid_msg, "不玩") != -1 or str.find(valid_msg, "退出") != -1:
        	return 1, '@' + self.player_name + " 虽然半途而废不怎么好听，但有时候放弃也是一种聪明的选择", self.shadiao_img
        random_num = random.randint(1, 3) - 1
        self.log.debug('random_num:{}'.format(random_num))
        self.log.debug('msg_code:{}'.format(self.msg_code[valid_msg]))
        #1：玩家 -1：机器人 0：平局
        winer = (random_num - self.msg_code[valid_msg]+ 4 )%3 - 1
        if winer == 0:
            return 0, self.draw_msg + " 目前比分：{}".format(self.com_score) + "-{}".format(self.player_score), self.rsp_img[random_num]
        else:
            can, res_msg = self.get_result(winer)
            return can, res_msg, self.rsp_img[random_num]
        
