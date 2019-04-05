# -*- coding: utf-8 -*-
import os
import random
import csv
from random import choice
from common.logger import Logger
from settings import DRAW_LOTS_WORDS_PATH

lots_dict = {}
words_dict = {}

class DrawLots(object):
    def __init__(self):
        self.log = Logger()
        '''获取抽签列表'''
        csv_file = csv.reader(open(DRAW_LOTS_WORDS_PATH, 'r', encoding='UTF-8'))
        for word in csv_file:
            lots_dict[word[0]] = word[1]
            words_dict[word[0]] = word[2]

    def play(self):       
        draw_random_num = random.randint(1, 20) - 1
        self.log.debug('draw_random_num:{}'.format(draw_random_num))
        return lots_dict[str(draw_random_num)], words_dict[str(draw_random_num)]
