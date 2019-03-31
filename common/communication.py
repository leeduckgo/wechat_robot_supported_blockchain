import requests

class Requester(object):
    def __init__(self, node):
        self.node = node

    def post(self, path, payload):
        url = self.node + path
        r = requests.post(url, json=payload)
        return r.json()

    def get(self, path, params = None):
        url = self.node + path
        r = requests.get(url, params=params)
        return r.json()

    def create_messages(self, group_name = '', name='',  content='', fans_id=''):
        """
        创建留言
        :param name:
        :param content: 留言内容
        :param fans_id:
        :return:
        """
        payload = {
            'name': name,
            'fans_id': fans_id,
            'context': content,
            'group_name': group_name
        }
        self.post("messages/create", payload)
        return "创建留言成功！点击链接查看：http://ycy.ahasmarter.com/msg"
