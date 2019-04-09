# -*- coding: utf-8 -*-
from common.communication import Requester

class RealEstate:

    def __init__(self):
        self.requester = Requester("http://ahasmarter.com/api/v1/ycy/")

    def look(self):
        raw_houses = self.requester.get("real_estates")
        return self.handle_raw_houses(raw_houses)
    def handle_raw_houses(self, raw_houses):
        houses_handled = ""
        for raw_house in raw_houses:
            house_string = "城堡: " + raw_house["name"] + "\n" +\
                "所有者：" + raw_house["owner"] + "\n" +\
                    "城堡上的签名：" + raw_house["signature"] + "\n" +\
                        "价格：" + str(raw_house["price"]) + "超越积分" + "\n" +\
                            "\n"
            houses_handled += house_string
        return houses_handled

    def leave_sig(self, user_puid, group_puid, content, name ,api_key):
        payload = {
            "api": api_key,
            "user": user_puid,
            "group_id": group_puid,
            "signature": content,
            "name": name            
        }
        return self.requester.post("real_estate/update", payload)

    def buy_house(self, user_puid, group_puid, name, amount, api_key):
        payload = {
            "api": api_key,
            "buyer": user_puid,
            "group_id": group_puid,
            "amount": amount,
            "name": name            
        }
        return self.requester.post("real_estate/buy/" + user_puid, payload)
