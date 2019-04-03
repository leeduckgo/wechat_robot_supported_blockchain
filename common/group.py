from common.communication import Requester
class Group:
    def __init__(self):
        pass
    def set_group(self, puid):
        self.puid = puid
        self.requester = Requester("http://ahasmarter.com/api/v1/ycy/")
        # self.intro =  self.get_intro()
        [self.intro,self.admin_puid] = self.get_intro()
        
    def get_intro(self):
        intro = self.requester.get("groups/" + self.puid)
        intro_modified = "群简介: " + intro['introduction'] + "\n" + \
                "群等级: " + str(intro['level']) + "\n"
        print(intro)
        # return intro_modified
        return [intro_modified, intro["admin_puid"]]
    
    def update_group(self, group, api_key):
        payload = {"group": {"level": 1, "introdcution" :"燃烧我的卡路里！", "puid": group.puid}}
        self.requester.post("users/create?api=" + api_key, payload)