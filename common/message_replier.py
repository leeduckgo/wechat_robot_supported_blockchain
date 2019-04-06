# -*- coding: utf-8 -*-
import os
import re
from random import choice

from wxpy import Tuling
from common.communication import create_messages
from common.group import Group
from common.logger import Logger
from common.rock_scissors_paper import RspGame
from common.user import User
from common.ycy_replier import YcyReplier
from common.draw_lots import DrawLots
from utils.utils import two_minutes_later
from utils.utils import now_to_datetime4

from secret import api_key,TULING_KEY

from apscheduler.schedulers.background import BackgroundScheduler

empty_result = ('', '', '')


class Replier(object):
    """消息回复"""

    level_map = {
        1: "隔壁村的幼稚鬼",
        2: "村子里的弟中弟",
        3: "村民中的初学者",
        4: "村子里的高中生",
        5: "合格的成年村民",
    }

    jokes = [
        '''美国外交代表团到苏联访问，苏修接待官员陪他们参观“建设的伟大成就”，并且得意的说：“到了下一个五年计划，每个苏联家庭都可以拥有一架私人飞机！”\n美国人惊讶的问：“ 他们要飞机干什么呢？”\n苏修官员说：“当然有用啊……譬如你在莫斯科听说列宁格勒开始供应面包了，你可以马上开飞机赶去排队啊。''',
        '''斯大林、赫鲁晓夫和勃列日涅夫乘坐火车出门。开着开着，火车突然停了。\n斯大林把头伸出车窗外，怒吼道：“枪毙火车司机！”可是车还是没有动。\n接着赫鲁晓夫说：“给火车司机恢复名誉！”车仍然没有动。\n勃列日涅夫说：“同志们，不如拉上窗帘，坐在座位上自己摇动身体，做出列车还在前进的样子……”''',
        '''美术馆里有一幅描写亚当和夏娃的画。\n一个英国人看了，说：“他们一定是英国人，男士有好吃的东西就和女士分享。\n一个法国人看了，说：“他们一定是法国人，情侣裸体散步。\n一个苏联人看了，说：“他们一定是苏联人，他们没有衣服，吃得很少，却还以为自己在天堂！'''
    ]

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
        self.user_lots_map = {}
        self.user_lots_read_map = {}
        '''
        开启每日定时器，每日零时清空抽签内容
        '''
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.init_lots_map, 'cron',  hour = '0')
        self.scheduler.start()

    def init_lots_map(self):
        """
        清空抽签内容，可以重新开始抽签
        """
        self.user_lots_map = {}
        self.user_lots_read_map = {}
        self.log.info("=== Init Lots ===")


    def random_img(self, msg)-> tuple:
        """
        随机获取图片
        :return:
        """
        if msg.text in ("天降超越",):  # todo 待增加
            list_dir = os.listdir(os.path.join('resources', 'pics'))
            path = choice(list_dir)
            self.log.info('choose:-->{}'.format(path))
            self.log.debug(os.path.join('resources', 'pics', path))
            return 'img', os.path.join('resources', 'pics', path), ''
        return empty_result

    def robot_init(self, msg)-> tuple:
        """
        机器人初始化
        :param msg:
        :return:
        """
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "初始化":
            if msg.member.puid == self.group.admin_puid:  # 如果是管理员
                self.log.info(msg.sender)
                # self.group.update_group(msg.sender, self.api_key)
                self.user.update_users(msg.sender, self.api_key)
                self.log.info("初始化完成！")
                return 'text', "初始化完成！", ''
            else:
                return 'text', "乃不是管理员啊", ''
        return empty_result

    def chaoyue_ana(self, msg)-> tuple:
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

    def handle_leave_message(self, msg)-> tuple:
        """
        处理留言
        :param msg:
        :return:
        """
        is_leave_message = re.search(r'(留言:|留言：)(.*)', msg.text)
        if is_leave_message:
            content = is_leave_message.group(2).strip()  # 获取第二组内容并去除前后空格
            self.log.info('留言内容:{}'.format(content))
            status = create_messages(
                name=msg.member.name,
                content=content,
                fans_id=msg.member.puid,
            )
            if status == "ok":
                return 'text', '@' + msg.member.name + ' ' + "留言成功！点击 {} 可查看你的留言".format(
                    'http://ycy.ahasmarter.com/',
                ), ''
            else:
                return 'text', '@' + msg.member.name + ' ' + "留言失败！稍后再尝试吧", ''
        return empty_result

    def get_group_introduction(self, msg)-> tuple:
        """
        获取群介绍
        :param msg:
        :return:
        """
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "群信息":
            return 'text', self.group.intro, ''
        return empty_result

    def finger_guessing_game(self, msg)-> tuple:
        """
        猜拳游戏
        :param msg:
        :return:
        """
        group_id = msg.member.group.puid  # 群组唯一id
        name = msg.member.name  # 玩家名
        user_id = msg.member.puid  # 玩家id
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "石头剪刀布" or real_msg[len(real_msg) - 1] == "剪刀石头布" \
                or real_msg[len(real_msg) - 1] == "猜拳":
            self.log.debug('---init猜拳----')
            # { 群组id : {玩家id: [游戏对象 , 开始游戏的时间, 玩家名]}}
            self.rsp_game_player_map.update(
                {
                    group_id: [user_id, RspGame(1), now_to_datetime4(), name],
                },
            )
            self.rsp_game_player_map[group_id][1].start(name)  # 开始游戏
            return 'text', '@' + msg.member.name + \
                   " 石头剪刀布开始，你先出吧，赢了我有奖励哦(1局定胜)", ''
        return empty_result

    def play_game(self, msg)-> tuple:
        """
        游戏
        :param msg:
        :return:
        """
        real_msg = msg.text.split()
        if "石头" in real_msg[len(real_msg) - 1]  or  "剪刀" in real_msg[len(real_msg) - 1]  \
                or "布" in real_msg[len(real_msg) - 1]:
            game = RspGame(1)
            game.start(msg.member.name)
            cancel, result, pic = game.play(msg)
            return 'both', pic, result
        else:
            return empty_result
        """
        group_id = msg.member.group.puid
        user_id = msg.member.puid
        player_map = self.rsp_game_player_map
        self.log.info(player_map)
        # 如果字典中包含群组id并且 玩家id在字典中
        if player_map.get(group_id):
            is_overtime = now_to_datetime4() > two_minutes_later(player_map[group_id][2])
            self.log.info('游戏是否超时:%s' % is_overtime)
            if is_overtime:
                msg = '@' + str(player_map[group_id][3]) + ' 游戏已经超时自动终止了呀!'
                msg.chat.send_msg(msg)
                player_map.pop(group_id)  # 超时删除群组id对应的字典
        if player_map.get(group_id):  # 超时可能会pop掉该key,需要重新判断
            if user_id not in player_map.get(group_id, []):  # 不是玩家的消息，不进行回应
                return 'text', '@' + msg.member.name + " 先等等哦，我正在跟@" + \
                       player_map[group_id][3] + " 玩石头剪刀布", ''
            else:
                cancel, result, pic = player_map[group_id][1].play(msg)  # 玩游戏
                self.log.debug('game result:{} pic:{}'.format(result, pic))
                if cancel == 1:
                    player_map.pop(group_id)  # 如果游戏结束, 删除群组id对应的字典
                return 'both', pic, result
        typ, content1, content2 = self.finger_guessing_game(msg)  # 猜拳游戏
        if typ == 'text':
            return typ, content1, content2
        return empty_result"""

    def draw_lots(self, msg)-> tuple:
        real_msg = msg.text.split()
        user_id = msg.member.puid
        if real_msg[len(real_msg) - 1] == "抽签":          
            if user_id in self.user_lots_map:
                return 'text', '@' + msg.member.name +' 今日你的运势签: ' + self.user_lots_map[user_id], ''
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

            
    def reward(self, msg)-> tuple:
        """
        打赏
        :param msg:
        :return:
        """
        if str.find(msg.text, "打赏") != -1:
            str_after_dashang = msg.text[str.find(msg.text, "打赏") + 3:].split()
            to = self.user.find_user_by_name(msg.sender, str_after_dashang[0])
            from_puid = msg.member.puid
            self.log.info(from_puid)
            self.log.info(to.puid)
            result = self.user.transfer(
                from_puid, to.puid, int(
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

    def integral(self, msg)-> tuple:
        """
        积分相关
        :return:
        """
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "超越积分":
            msg = "超越积分可以用来干很多好玩的事情。"
            return 'text', msg, ''
        if real_msg[len(real_msg) - 1] in ["余额", "积分"]:
            user_puid = msg.member.puid
            print("想拿余额的puid:")
            print(user_puid)
            balance = self.user.get_balance_by_puid(user_puid)
            msg = "你有" + str(balance) + "超越积分"
            return 'text', msg, ''
        if real_msg[len(real_msg) - 1] == "等级":
            user_puid = msg.member.puid
            level = self.user.get_level_by_puid(user_puid)
            msg = "你现在是" + str(level) + "级: " + self.level_map[int(level)]
            return 'text', msg, ''
        return empty_result

    def extra(self, msg)-> tuple:
        """
        额外添加
        :param msg:
        :return:
        """
        real_msg = msg.text.split()
        if real_msg[len(real_msg) - 1] == "致谢":
            return 'text', "感谢「心理医生聪」，提供超越语录的支持！", ''
        if real_msg[len(real_msg) - 1] in ["帮助","?","？"]:
            payload = "本 AI 目前支持以下功能: \n" + \
                        "- 超越积分\n" + \
                        "- 天降超越\n" + \
                        "- 超越猜拳\n" + \
                        "- 村头留言板\n" + \
                        "- 超越抽签\n" + \
                        "- 成语接龙\n"
                    
            return 'text', payload, ''
        if real_msg[len(real_msg) - 1] == "投票":
            payload = "https://ke.qq.com/course/392391?tuin=ce503a40 ⬅ 欢迎猛戳链接投票"
            return 'text', payload, ''
        if real_msg[len(real_msg) - 1].find("笑话") != -1:
            payload = choice(self.jokes)
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

    def handle_group_msg(self, msg)-> tuple:
        """
        处理群组回复消息
        :param msg:
        :return:
        """
        self.log.info('receive: %s' % msg.text)

        typ, content1, content2 = self.reward(msg)  # 打赏可能被@ 也可能不被@
        if typ:
            self.log.info(content1)
            return typ, content1, content2
        typ, content1, content2 = self.random_img(msg)  # 天降超越
        if typ:
            self.log.info(content1)
            return typ, content1, content2
        typ, content1, content2 = self.chaoyue_ana(msg)  # 超越语录
        if typ:
            self.log.info(content1)
            return typ, content1, content2

        if msg.is_at:  # 如果@到机器人，才进行的回应
            typ, content1, content2 = self.robot_init(msg)  # 初始化最高优先级
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            typ, content1, content2 = self.play_game(msg)  # 玩游戏,高优先级,内部存在拦截其他回复
            if typ:
                self.log.info(content1)
                user_puid = msg.member.puid
                bot_id = self.bot.self.puid
                user_balance = self.user.get_balance_by_puid(user_puid)
                bot_balance = self.user.get_balance_by_puid(bot_id)
                if user_balance < 3:
                    payload = " 由于你余额不足 3 积分，所以本次游戏没有奖惩哦~"
                elif bot_balance < 3:
                    payload = " 超越宝宝的钱包瘪了，所以本次游戏没有奖惩哦~"
                else:
                    if "游戏结束，恭喜你赢了" in content2:
                        from_puid = bot_id
                        print(from_puid)
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
            typ, content1, content2 = self.draw_lots(msg)  # 抽签
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            typ, content1, content2 = self.handle_leave_message(msg)  # 处理留言请求
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            typ, content1, content2 = self.get_group_introduction(msg)  # 群简介
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            typ, content1, content2 = self.integral(msg)  # 积分相关
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            typ, content1, content2 = self.extra(msg)  # 额外信息
            if typ:
                self.log.info(content1)
                return typ, content1, content2
            tuling_reply = self.tuling.reply_text(msg).replace("图灵机器人", "超越宝宝").replace("清华大学硕士杨超？", "杨超越最美不允许反驳")
            self.log.info(tuling_reply)
            return 'text', tuling_reply, ''

        return empty_result
