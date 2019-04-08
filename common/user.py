# -*- coding: utf-8 -*-
from common.communication import Requester


class User(object):
    def __init__(self):
        self.requester = Requester("http://ahasmarter.com/api/v1/ycy/")

    def get_balance_by_puid(self, puid, group_puid):
        user = self.requester.get("users/" + puid +"?group_id=" + group_puid)
        return user["balance"]

    def get_level_by_puid(self, puid, group_puid):
        user = self.requester.get("users/" + puid + "?group_id=" + group_puid)
        return user["level"]

    def find_user_by_name(self, group, name):
        for member in group.members:
            if name in member.name:
                return member

    def transfer(self, from_puid, to_puid, group_puid, amount, api_key):
        payload = {
            "from": from_puid,
            "to": to_puid,
            "amount": amount,
            "group_id": group_puid
        }
        return self.requester.post("users/transfer?api=" + api_key, payload)

    def update_users(self, group, api_key):
        members = group.members
        users = []
        for member in members:
            user = {
                "name": member.name,
                "puid": member.puid,
                "level": 1,
                "balance": 0,
            }
            users.append(user)
        payload = {"group": group.puid, "users": users}
        self.requester.post("users/create?api=" + api_key, payload)
