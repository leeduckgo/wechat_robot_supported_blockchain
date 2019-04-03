# -*- coding: utf-8 -*-
from common.communication import Requester

class Group:

    level_map = {
        1: "芝麻大的小村庄",
        2: "核桃大的中村庄",
        3: "西瓜大的大村庄",
        4: "村中之村",
        5: "村中之村中之村"
    }
    def __init__(self):
        self.requester = Requester("http://ahasmarter.com/api/v1/ycy/")
        self.puid = None
        self.intro = None
        self.admin_puid = None

    def set_group(self, puid):
        self.puid = puid
        # self.intro =  self.get_intro()
        self.intro, self.admin_puid = self.get_intro()

    def get_intro(self):
        intro = self.requester.get("groups/" + self.puid)
        intro_modified = "群简介: " + intro['introduction'] + "\n" + \
                         "群等级: " + self.level_map[intro['level']] + "\n"
        # return intro_modified
        return intro_modified, intro["admin_puid"]

    # def handle_level(self, level):
        
    def update_group(self, group, api_key):
        payload = {
            "group": {
                "level": 1,
                "introdcution": "燃烧我的卡路里！",
                "puid": group.puid,
            },
        }
        self.requester.post("users/create?api=" + api_key, payload)
