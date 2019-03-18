# -*- coding: utf-8 -*-
from settings import RESOURCES_PATH
import csv
import jieba
import jieba.analyse
from common.logger import Logger

QA_dict = {}

class YcyReplier(object):
    def __init__(self):
        self.log = Logger()
        '''训练QA样本，获得QA映射表'''
        csv_file = csv.reader(open(RESOURCES_PATH, 'r', encoding='UTF-8'))
        for QA in csv_file:
            tags = jieba.analyse.extract_tags(QA[0], topK=3)
            key = ''
            for tag in tags:
                key += tag
            if (len(key)):
                QA_dict[key] = QA[1]
            else:
                QA_dict[QA[0]] = QA[1]
        self.log.info("Dict:{}".format(QA_dict))

    def reply_text(self, msg):
        tags = jieba.analyse.extract_tags(msg, topK=3)
        key = ''
        for tag in tags:
            key += tag
        self.log.info("KeyWords:{}".format(key))
        if (len(key)):
            if key in QA_dict:
                return (QA_dict[key])
            else:
                return
        else:
            if msg in QA_dict:
                return (QA_dict[msg])
            else:
                return
