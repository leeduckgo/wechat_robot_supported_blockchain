# -*- coding: utf-8 -*-
from random import choice
import os
import re
from wxpy import Tuling
from common.logger import Logger
from common.ycy_replier import YcyReplier
from common.rock_scissors_paper import RspGame
from settings import TULING_KEY
from common.group import Group
from common.user import User
class Replier(object):
    """消息回复"""
    def __init__(self, api_key):
        # self.group = group
        self.log = Logger()
        self.ycy = YcyReplier()
        self.tuling = Tuling(api_key=TULING_KEY)
        self.rsp_game = RspGame(5)
        self.rsp_game_player_name = ''
        self.rsp_game_flag = False #是否开启石头剪刀布游戏
        self.group = Group()
        self.user = User()
        self.api_key = api_key

    def set_group(self, puid):
        self.group.set_group(puid)
    def random_img(self):
        """随机获取图片"""
        list_dir = os.listdir(os.path.join('resources', 'pics'))
        path = choice(list_dir)
        self.log.info('choose:-->{}'.format(path))
        return os.path.join("resources", "pics", path)
    
    def leave_message(self, msg):
        """处理留言"""
        is_leave_message = re.search(r'(留言:|留言：)(.*)', msg.text)

        if is_leave_message:
            content = is_leave_message.group(2).strip()  # 获取第二组内容并去除前后空格
            self.log.info('留言内容:{}'.format(content))
            result = self.group.requester.create_messages(group_name="内测群", name=msg.member.name, content=content, fans_id=msg.member.puid)
            return result


    def handle_msg(self, msg):
        """进行游戏"""
        if  self.rsp_game_flag:
            if not msg.is_at:#如果没有@到机器人，不进行回应
                return '', '', ''
            elif self.rsp_game_player_name != msg.member.display_name:#不是玩家的消息，不进行回应
                return 'text', '@' + msg.member.display_name + " 先等等哦，我正在跟@" + self.rsp_game_player_name+ " 玩石头剪刀布", ''
            else:             
                cancel, result, pic = self.rsp_game.play(msg)
                self.log.debug('game result:{} pic:{}'.format(result, pic))
                if cancel == 1:
                    self.rsp_game_flag = False
                return 'both', pic, result

        """处理回复消息"""
        self.log.info(msg)
        if msg.text == "天降超越":
            path = self.random_img()
            self.log.debug(path)
            # self.group.send_image(path)
            return 'img', path, ''
        if str.find(msg.text, "燃烧") != -1:
            # self.group.send()
            return 'text', "燃烧我的卡路里！", ''
        if str.find(msg.text, "打赏") != -1:
            str_after_dashang = msg.text[str.find(msg.text, "打赏") + 3:].split()
            to = self.user.find_user_by_name(msg.sender, str_after_dashang[0])
            from_puid = msg.member.puid
            print(from_puid)
            print(to.puid)
            result = self.user.transfer(from_puid, to.puid, int(str_after_dashang[1]), self.api_key)
            if result["status"] == "success":
                payload = '打赏成功！'+ msg.member.name + " 打赏给 " + to.name + " " + str_after_dashang[1] + "个超越积分！"
                return 'text', payload, ''
            else:
                return 'text', '打赏失败！', ''
        if not msg.is_at:  # 如果没有@到机器人，不进行回应
            return '', '', ''
        else:
            real_msg = msg.text.split()
            print(real_msg[len(real_msg)-1])
            self.log.debug("send:"+real_msg[len(real_msg)-1])
            if real_msg[len(real_msg)-1] == "群信息":
                return 'text', self.group.intro, ''
            if real_msg[len(real_msg)-1] == "致谢":
                return 'text', "感谢「心理医生聪」，提供超越语录的支持！", ''
            if real_msg[len(real_msg)-1] == "帮助":
                payload = "本 AI 目前支持以下功能: \n" +\
                    "- 超越积分\n" + \
                        "- 天降超越\n" + \
                            "- 超越猜拳\n" + \
                                "- 村头留言板\n"
                return 'text', payload, ''    
            if real_msg[len(real_msg)-1] == "余额":
                user_puid = msg.member.puid
                balance = self.user.get_balance_by_puid(user_puid)
                msg = "你有" + str(balance) + "超越积分"
                return 'text', msg, ''
            if real_msg[len(real_msg)-1] == "等级":
                user_puid = msg.member.puid
                balance = self.user.get_level_by_puid(user_puid)
                msg = "你现在是" + str(balance) + "级"
                return 'text', msg, ''
            if real_msg[len(real_msg)-1] == "天降超越":
                path = self.random_img()
                self.log.debug(path)
                # self.group.send_image(path)
                return 'img', path, ''
            if real_msg[len(real_msg)-1].find("留言") != -1: # 村头留言板
                payload = self.leave_message(msg)       
                return 'text', payload, ''
            if real_msg[len(real_msg)-1] == "初始化":
                if msg.member.puid == self.group.admin_puid: # 如果是管理员
                    print(msg.sender)
                    # self.group.update_group(msg.sender, self.api_key)
                    self.user.update_users(msg.sender, self.api_key)
                    print("初始化完成！")
                    return 'text', "初始化完成！", ''
                else:
                    return 'text', "乃不是管理员啊", ''              
            if real_msg[len(real_msg)-1] == "石头剪刀布" or  real_msg[len(real_msg)-1] == "剪刀石头布" \
            or  real_msg[len(real_msg)-1] == "猜拳":                
                self.rsp_game_player_name = msg.member.display_name
                self.rsp_game.start(msg.member.display_name)
                self.rsp_game_flag = True
                return 'text', '@' + msg.member.display_name + " 石头剪刀布开始，你先出吧，赢了我有奖励哦(一局一胜)", ''
            respond_msg = self.ycy.reply_text(real_msg[len(real_msg) - 1])
            if respond_msg:
                return 'text', '@' + msg.member.display_name + ' ' + respond_msg, ''
            else:
                return 'text', self.tuling.reply_text(msg).replace("图灵机器人", "超越宝宝"), ''
