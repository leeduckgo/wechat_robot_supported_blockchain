import requests


class Requester(object):
    def __init__(self, node):
        self.node = node

    def post(self, path, payload):
        url = self.node + path
        r = requests.post(url, json=payload)
        return r.json()

    def get(self, path, params):
        url = self.node + path
        r = requests.get(url, params=params)
        return r.json()
