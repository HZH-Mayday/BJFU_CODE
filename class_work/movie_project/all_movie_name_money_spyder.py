# -*- coding:utf-8 -*-
import sys
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import csv
import json
from pprint import pprint
import re


def get_movie_name_money(page, area):
    '''
    爬取 http://www.cbooo.cn/movies 中的电影名字和票房
    :param page: (int) 爬取的页码 (1,2,3....)
    :param area: (int) 地区代码 (1 美国，50 中国)
    :return: (dict) 电影的信息字典，{名字，票房，日期}
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102',
               'Host': 'www.cbooo.cn',
               'Referer': 'http://www.cbooo.cn/movies',}
    params = {"area": area, "type": 0, "year": 0, "initial": "全部", "pIndex": page}
    base_url = "http://www.cbooo.cn/Mdata/getMdata_movie?"
    name_money_json = requests.request(method="GET", url=base_url, params=params, headers=headers).json()
    # pprint(name_money_json)

    # 提取电影名字和票房
    return_list = []
    for one_movie in name_money_json["pData"]:
        year = one_movie["releaseYear"]
        name = one_movie["MovieName"]
        money = one_movie["BoxOffice"]
        return_list.append([name, money, year])

    return return_list

if __name__ == "__main__":

    # x = get_movie_name_money(1)
    # print(x)

    for i in range(1, 21):
        with open("./movie_data/movie_money_info_USA.csv", "a+", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            input_list = get_movie_name_money(i, 1)
            writer.writerows(input_list)
            print(i)
            sleep(np.random.randint(0,2))


