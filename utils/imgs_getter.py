"""
获取YCY图片
"""
import requests
import json


class YCYImage(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            # "Content-Type": "application/x-www-form-urlencoded",
        }
        
    def get_img(self):
        """获取100页的图片链接"""
        url = "https://www.duitang.com/napi/blog/list/by_search/"
        result = []
        for page in range(0, 240, 24):
            data = {
                'kw': '杨超越',
                'type': 'feed',
                'include_fields': 'top_comments,is_root,source_link,item,buyable,root_id,status,like_count,like_id,sender,album,reply_count,favorite_blog_id',
                '_type': '',
                'start': str(page),
            }
            r = requests.get(url, headers=self.headers, params=data, verify=False)
            d = json.loads(r.text)
            if d.get('data').get('object_list'):
                d = d['data']['object_list']
                result.extend(d)
        return result

    def download_img_and_save(self, result):
        """下载图片并保存"""
        if not result:
            print('未爬取到图片')
            return
        for index, d in enumerate(result):
            r = requests.get(url=d['photo']['path'])
            with open('pics/ycy_{}.jpg'.format(index), 'wb') as f:
                f.write(r.content)

    def run(self):
        result = self.get_img()
        self.download_img_and_save(result)


if __name__ == '__main__':
    ycy = YCYImage()
    ycy.run()
