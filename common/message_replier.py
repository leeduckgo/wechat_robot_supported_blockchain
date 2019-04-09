# -*- coding: utf-8 -*-
import os
import re
from random import choice
from functools import wraps
from wxpy import Tuling
from common.communication import create_messages
from common.group import Group
from common.logger import Logger
from common.rock_scissors_paper import RspGame
from common.user import User
from common.real_estate import RealEstate
from common.ycy_replier import YcyReplier
from common.draw_lots import DrawLots
from common.const import q_a_list
from common.const import jokes
from common.const import level_map
# from utils.utils import two_minutes_later
# from utils.utils import now_to_datetime4

from secret import api_key
from secret import TULING_KEY

from apscheduler.schedulers.background import BackgroundScheduler

empty_result = ('', '', '')


def extend_finger_guessing(func):
    """
    扩展猜拳游戏
    :param func:
    :return:
    """
    @wraps(func)
    def inner(self, msg):
        typ, content1, content2 = func(self, msg)
        if typ:
            if typ == 'text':
                return typ, content1, content2
            user_puid = msg.member.puid
            bot_id = self.bot.self.puid
            user_balance = self.user.get_balance_by_puid(user_puid, self.group.puid, msg)
            bot_balance = self.user.get_balance_by_puid(bot_id, self.group.puid)
            if user_balance < 3:
                payload = " 由于你余额不足 3 积分，所以本次游戏没有奖惩哦~"
            elif bot_balance < 3:
                payload = " 超越宝宝的钱包瘪了，所以本次游戏没有奖惩哦~"
            else:
                if "游戏结束，恭喜你赢了" in content2:
                    from_puid = bot_id
                    to_puid = user_puid
                    result = self.user.transfer(from_puid, to_puid, 3, self.api_key)
                    if result["status"] == "success":
                        payload = " 奖励给 " + msg.member.name + " 3 个超越积分！"
                    else:
                        payload = " 但是我没钱啦~"
                elif "你输了" in content2:
                    from_puid = user_puid
                    to_puid = bot_id
                    result = self.user.transfer(from_puid, to_puid, 3, self.api_key)
                    if result["status"] == "success":
                        payload = " 扣除 " + msg.member.name + " 3 个超越积分！"
                    else:
                        payload = " 你钱不够，接下来的游戏会没有奖励哦~"
                else:
                    payload = ""
            return typ, content1, content2 + payload
        return empty_result

    return inner


class Replier(object):
    """消息回复"""

    def __init__(self, bot):
        # self.group = group
        self.api_key = api_key
        self.log = Logger()
        self.ycy = YcyReplier()
        self.tuling = Tuling(api_key=TULING_KEY)
        self.user = User()
        self.group = Group()
        self.rsp_game_player_map = {}
        self.bot = bot
        self.draw_lots_game = DrawLots()
        self.real_estate = RealEstate()
        self.user_lots_map = {}
        self.user_lots_read_map = {}
        self.answer = ""
        self.red_bag_num = 0

        # 开启每日定时器，每日零时清空抽签内容
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.init_lots_map, 'cron', hour='0')
        self.scheduler.start()

    def init_lots_map(self):
        """
        清空抽签内容，可以重新开始抽签
        """
        self.user_lots_map = {}
        self.user_lots_read_map = {}
        self.log.debug("=== Init Lots ===")

    def random_img(self, msg) -> tuple:
        """
        随机获取图片
        :return:
        """
        self.log.debug("===天降超越===")
        self.log.debug(msg.text)

        if "天降超越" in msg.text or "天将超越" in msg.text:  # todo 待增加
            list_dir = os.listdir(os.path.join('resources', 'pics'))
            path = choice(list_dir)
            self.log.debug('choose:-->{}'.format(path))
            self.log.debug(os.path.join('resources', 'pics', path))
            return 'img', os.path.join('resources', 'pics', path), ''
        return empty_result

    def robot_init(self, msg) -> tuple:
        """
        机器人初始化
        :param msg:
        :return:
        """
        real_msg = msg.text.split()
        if msg.member.puid == self.group.admin_puid and len(real_msg) != 1:  # 如果是管理员
            if real_msg[len(real_msg) - 1] == "初始化":
                self.log.debug(msg.sender)
                # self.group.update_group(msg.sender, self.api_key)
                self.update_user_info(msg)
                self.log.debug("初始化完成！")
                return 'text', "初始化完成！", ''
            elif real_msg[1] == "口令红包":
                self.log.debug("设置口令红包！")
                self.log.debug("===口令红包信息===")
                self.log.debug(real_msg[2])
                self.log.debug(real_msg[3])
                try:
                    self.red_bag_num = int(real_msg[2])
                except:
                    self.red_bag_num = 0
                if real_msg[3] in q_a_list:
                    item = q_a_list[real_msg[3]]
                    self.answer = item[1]
                    return 'text', item[0], ''
                else:
                    self.answer = real_msg[3]
                    return 'text', "口令红包设置完成！", ''
            else:
                return empty_result
        return empty_result

    def update_user_info(self, msg):
        self.log.debug("更新用户信息中……")
        self.user.update_users(msg=msg)
        self.log.debug("用户信息更新完毕……")

    def chaoyue_ana(self, msg) -> tuple:
        """
        超越语录
        :return:
        """
        real_msg = msg.text.split()
        respond_msg = self.ycy.reply_text(real_msg[len(real_msg) - 1])  # 超越语录无需要@
        if respond_msg:
            return 'text', '@' + msg.member.name + ' ' + respond_msg, ''
        return empty_result

    def set_group(self, puid):
        self.group.set_group(puid)

    def handle_leave_message(self, msg) -> tuple:
        """
        处理留言
        :param msg:
        :return:
        """
        if "村头留言板" in msg.text:
            return "text", "@我并回复:「留言:你想说的话」，则可在村头留言板上留下你的留言内容哦", ""
        is_leave_message = re.search(r'(留言:|留言：)(.*)', msg.text)
        if is_leave_message:
            content = is_leave_message.group(2).strip()  # 获取第二组内容并去除前后空格
            self.log.debug('留言内容:{}'.format(content))
            status = create_messages(
                name=msg.member.name,
                content=content,
                fans_id=msg.member.puid,
            )
            if status == "ok":
                return 'text', '@' + msg.member.name + ' ' + "留言成功！点击 {} 可查看你的留言".format(
                    'http://ahasmarter.com/',
                ), ''
            else:
                return 'text', '@' + msg.member.name + ' ' + "留言失败！稍后再尝试吧", ''
        return empty_result

    def get_group_introduction(self, msg) -> tuple:
        """
        获取群介绍
        :param msg:
        :return:
        """
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "群信息" or real_msg[len(real_msg) - 1] == "群简介":
            return 'text', self.group.intro, ''
        return empty_result

    @extend_finger_guessing
    def finger_guessing_game(self, msg) -> tuple:
        """
        猜拳游戏
        :param msg:
        :return:
        """
        if "超越猜拳" in msg.text:
            return "text", "@我并回复你的出招(比如「剪刀」)就能跟我玩猜拳游戏，赢了我会奖励3积分，输了扣除3积分，如果积分不够则不会进行奖惩", ""
        real_msg = msg.text.split()
        if "石头" in real_msg[len(real_msg) - 1] or "剪刀" in real_msg[len(real_msg) - 1] \
                or "布" in real_msg[len(real_msg) - 1]:
            game = RspGame(1)
            game.start(msg.member.name)
            cancel, result, pic = game.play(msg)
            return 'both', pic, result
        else:
            return empty_result

    def red_bag(self, msg) -> tuple:
        """
        口令红包
        :param msg:
        :return:
        """

        if "口令红包" in msg.text:
            return "text", "管理员会在某些时间在群里发出超越百科抢答红包，回答正确会得到超越积分，多多留意~", ""
        real_msg = msg.text.split()
        if self.red_bag_num == 0:  # 如果红包剩余数量为0
            self.answer = ""  # answer清零
        else:
            print(self.answer)
            if self.answer == real_msg[1] and msg.is_at:
                user_puid = msg.member.puid
                bot_id = self.bot.self.puid
                result = self.user.transfer(bot_id, user_puid, self.group.puid, 3, self.api_key)
                self.red_bag_num -=1
                if result["status"] == "success":
                    return 'text'," 口令正确！奖励给" + msg.member.name + " 3 个超越积分！", ''
                else:
                    return 'text', '红包领完啦！', ''
        return empty_result

    def draw_lots(self, msg) -> tuple:
        """
        超越抽签
        :param msg:
        :return:
        """
        if "超越抽签" in msg.text:
            return "text", "每日0点过后，@我并回复「抽签」，可以抽出你当日的运势签，@我并回复「解签」会解释抽签内容~", ""
        real_msg = msg.text.split()
        user_id = msg.member.puid
        if real_msg[len(real_msg) - 1] == "抽签":
            if user_id in self.user_lots_map:
                return 'text', '@' + msg.member.name + ' 今日你的运势签: ' + self.user_lots_map[user_id], ''
            else:
                msg1, msg2 = self.draw_lots_game.play()
                self.user_lots_map[user_id] = msg1
                self.user_lots_read_map[user_id] = msg2
                return 'text', '@' + msg.member.name + ' 今日你的运势签: ' + msg1, ''
        elif real_msg[len(real_msg) - 1] == "解签":
            if user_id in self.user_lots_read_map:
                return 'text', '@' + msg.member.name + ' 解签: ' + self.user_lots_read_map[user_id], ''
            else:
                return 'text', '@' + msg.member.name + ' 今日还未进行抽签哦，请@我回复抽签', ''
        else:
            return empty_result

    def reward(self, msg) -> tuple:
        """
        打赏
        :param msg:
        :return:
        """
        if str.find(msg.text, "打赏") != -1:
            str_after_dashang = msg.text[str.find(msg.text, "打赏") + 3:].split()
            to = self.user.find_user_by_name(msg.sender, str_after_dashang[0])
            from_puid = msg.member.puid
            self.log.debug(from_puid)
            self.log.debug(to.puid)
            result = self.user.transfer(
                from_puid, to.puid, self.group.puid, int(
                    str_after_dashang[1],
                ), self.api_key,
            )
            if result["status"] == "success":
                payload = '打赏成功！' + msg.member.name + " 打赏给 " + \
                          to.name + " " + str_after_dashang[1] + "个超越积分！"
                return 'text', payload, ''
            else:
                return 'text', '打赏失败！', ''
        return empty_result

    def integral(self, msg) -> tuple:
        """
        积分相关
        :return:
        """
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "超越积分":
            msg = "超越积分可以用来干很多好玩的事情，后续推出虚拟房产和虚拟商店，可作为购买力进行交易哦，还支持个人打赏，@我并回复「余额」来查看你的积分总额。"
            return 'text', msg, ''
        if real_msg[len(real_msg) - 1] in ["余额", "积分"]:
            user_puid = msg.member.puid
            self.log.debug("想拿余额的puid:")
            self.log.debug(user_puid)
            balance = self.user.get_balance_by_puid(user_puid, self.group.puid, msg)
            msg = "你有" + str(balance) + "超越积分"
            return 'text', msg, ''
        if real_msg[len(real_msg) - 1] == "等级":
            user_puid = msg.member.puid
            level = self.user.get_level_by_puid(user_puid, self.group.puid, msg)
            msg = "你现在是" + str(level) + "级: " + level_map[int(level)]
            return 'text', msg, ''
        return empty_result

    def houses(self, msg)-> tuple:
        """
        房产相关
        :return:
        """
        real_msg = msg.text.split()
        try:
            if "超越买房" in msg.text:
                return "text", "超越买房是实验性功能，@我并回复「看房」查看目前「超越大陆」上的房产所有者\n\n"+\
                    "@我并回复「买房 房产名 价格」可以进行房产购买，例如「@全村的希望 买房 火炉堡 30」\n"+\
                        "注意！！！你出的价格至少要比当前的价格大 1，才能买房成功 \n" +\
                        "如果你是房产所有者，@我并回复「房产名 签名：「你要签名的内容」」可进行签名，例如「@全村的希望 火炉堡 签名：靓仔」", ""
            if real_msg[len(real_msg) - 1] == "看房":
                self.log.debug("=== 看房ing ===")
                msg = self.real_estate.look()
                return 'text', msg, ''
            elif re.search(r'(签名:|签名：)(.*)', msg.text):
                self.log.debug("=== 签名ing ===")
                house_name = real_msg[1]
                self.log.debug(msg.text)
                signature = msg.text[msg.text.find("签名")+3:]
                self.log.debug(house_name)
                self.log.debug(self.api_key)
                self.log.debug(msg.member.puid)
                self.log.debug(self.group.puid)
                self.log.debug(signature)
                res = self.real_estate.leave_sig(msg.member.puid, self.group.puid, signature, house_name, self.api_key)
                self.log.debug(res)
                if res["result"] == "success":
                    payload = "你在" + house_name + "上留下了你的签名：" + signature
                    return 'text', payload, ''
                else:
                    payload = "签名失败！"
                    return 'text', payload, ''
            elif real_msg[1] == "买房":
                self.log.debug("=== 买房ing ===")
                house_name = real_msg[2]
                amount = int(real_msg[3])
                self.log.debug(house_name)
                self.log.debug(amount)
                res = self.real_estate.buy_house(msg.member.puid, self.group.puid, house_name, amount, self.api_key)
                if res["result"] == "success":
                    payload = "买房成功！\n你现在是 " + house_name + " 的领主！"
                    return 'text', payload, ''
                else:
                    payload = "买房失败！"
                    return 'text', payload, ''

            return empty_result
        except:
            return empty_result

    def extra(self, msg)-> tuple:
        """
        额外添加
        :param msg:
        :return:
        """
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] in ["致谢", "鸣谢"]:
            return 'text', "感谢「心理医生聪」与「禹sen」，提供超越语录的支持！", ''
        if real_msg[len(real_msg) - 1] in ["帮助", "?", "？"]:
            payload = "本 AI 目前支持以下功能: \n" + \
                        "- 超越积分\n" + \
                        "- 天降超越\n" + \
                        "- 超越猜拳\n" + \
                        "- 村头留言板\n" + \
                        "- 超越抽签\n" + \
                        "- 超越接龙\n" + \
                        "- 口令红包（管理员功能）\n" + \
                        "- 超越买房"

            return 'text', payload, ''
        if real_msg[len(real_msg) - 1] == "投票":
            payload = "https://ke.qq.com/cates/ccyy/index.html?act_id=1&work_id=29&mmticket= ⬅ 欢迎猛戳链接投票"
            return 'text', payload, ''
        if real_msg[len(real_msg) - 1].find("笑话") != -1:
            payload = choice(jokes)
            return 'text', payload, ''
        return empty_result

    def handle_solo_msg(self, msg):
        """
        处理私聊回复
        :param msg:
        :return:
        """
        friend = msg.sender
        # 向新的好友发送消息
        friend.send('你好呀,我是全村的希望!')
        friend.send('参与内测看我朋友圈的图片,扫二维码加群')
        # friend.send_image('group.jpeg')

    @property
    def at_or_not_at_list(self) -> list:
        """
        优先级: at_or_not_at_list > only_at_list = only_not_at_list
        无论是否被@都会执行,最高优先级
        根据优先级排列顺序
        :return:
        """
        funcs = [
            self.robot_init,  # 紧急情况下的初始化以及口令红包的初始化
            self.reward,  # 打赏可能被@ 也可能不被@
            self.red_bag,  # 口令红包
            self.random_img,  # 天降超越
            self.chaoyue_ana,  # 超越语录
        ]
        return funcs

    @property
    def only_at_list(self) -> list:
        """
        被@时触发的功能,优先级小于at_or_not_at_list
        根据优先级排列顺序
        :return:
        """
        funcs = [
            self.finger_guessing_game,  # 猜拳游戏
            self.random_img,  # 被@时也能触发天降超越
            self.draw_lots,  # 超越抽签
            self.handle_leave_message,  # 处理留言
            self.get_group_introduction,  # 群组简介
            self.integral,  # 超越积分
            self.extra,  # 额外信息
            self.houses,
        ]
        return funcs

    @property
    def only_not_at_list(self) -> list:
        """
        仅未被@时触发的功能优先级等于only_at_list
        根据优先级排列顺序
        :return:
        """
        funcs = [
            # self.test
        ]
        return funcs

    def handle_group_msg(self, msg) -> tuple:
        """
        处理群组回复消息
        :param msg:
        :return:
        """
        self.log.debug('receive: %s' % msg.text)

        for func in self.at_or_not_at_list:
            typ, content1, content2 = func(msg)
            if typ:
                self.log.debug(content1)
                return typ, content1, content2

        if msg.is_at:  # 如果@到机器人，才进行的回应
            for func in self.only_at_list:
                typ, content1, content2 = func(msg)
                if typ:
                    self.log.debug(content1)
                    return typ, content1, content2
            tuling_reply = self.tuling.reply_text(msg).replace("图灵机器人", "超越宝宝").replace(
                "清华大学硕士杨超？", "杨超越最美不允许反驳"
            ).replace("你接错了", "我不会接")
            self.log.debug(tuling_reply)
            return 'text', tuling_reply, ''
        else:  # 预留仅未被@时执行,暂无此情况
            for func in self.only_not_at_list:
                typ, content1, content2 = func(msg)
                if typ:
                    self.log.debug(content1)
                    return typ, content1, content2

        return empty_result
