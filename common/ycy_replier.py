from settings import RESOURCES_PATH
import csv
import jieba
import jieba.analyse

QA_dict = {}

class YcyReplier(object):
    def __init__(self):
        csv_file = csv.reader(open(RESOURCES_PATH, 'r', encoding='UTF-8'))
        for QA in csv_file:
            '''cut_words = jieba.cut(QA[0], cut_all = False)
            print("分词结果： " + ", ".join(cut_words))'''
            tags = jieba.analyse.extract_tags(QA[0], topK=3)
            key = ''
            for tag in tags:
                key += tag
            if(len(key)):
                QA_dict[key] = QA[1]
            else:
                QA_dict[QA[0]] = QA[1]
        print(QA_dict)


    def do_reply(slef, msg):
        tags = jieba.analyse.extract_tags(msg, topK=3)
        key = ''
        for tag in tags:
            key += tag
        if(len(key)):
            if key in QA_dict:
                return(QA_dict[key])
            else:
                return
        else:
            if msg in QA_dict:
                return(QA_dict[msg])
            else:
                return



