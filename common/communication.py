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


def create_messages(name='',  content='', fans_id='',):
    """
    创建留言
    :param name:
    :param content: 留言内容
    :param fans_id:
    :return:
    """
    url = 'http://ahasmarter.com/api/v1/ycy/messages/create'
    data = {
        'name': name,
        'fans_id': fans_id,
        'context': content,
    }
    r = requests.post(url, json=data)
    return r.status_code


def get_group_introduction(puid=''):
    """
    获取群介绍
    :param name:
    :param content: 留言内容
    :param fans_id:
    :return:
    """
    url = 'http://ahasmarter.com/api/v1/ycy/groups/' + str(puid)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json
    return {}
