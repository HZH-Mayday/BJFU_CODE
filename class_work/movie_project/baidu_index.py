# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from pprint import pprint
from urllib.parse import quote
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm
import csv
from datetime import datetime
from time import sleep


def index_select(name):
    '''
    查询name的百度指数
    :param name: (string) 想要知道百度指数的名字
    :return: (int) 百度指数
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102',
               'Cookie': '''BIDUPSID=6056EEEFEDC9E926B361B3FD640FA228; PSTM=1535259366; BAIDUID=7594899E950731CA9001784A21AF1EE4:FG=1; BDUSS=nczekl1fk1aNnl4cWFhdkY3QnRocWNCZlhMMXZ0OXR1NmY0TlFzTldDTE1RYXBiQVFBQUFBJCQAAAAAAAAAAAEAAAACWfhUuf7C3nF3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMy0glvMtIJbR; MCITY=-131%3A; pgv_pvi=9144667136; cflag=15%3A3; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; bdindexid=tca8sosplscmnisi61d422ses5; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=1; H_PS_PSSID=26525_1465_21096_20698_20719; BDSFRCVID=9OtsJeCCxG37sLJ7gAYG81gcU0FOeQZRddMu3J; H_BDCLCKID_SF=tR30WJbHMTrDHJTg5DTjhPrMetnJbMT-027OKK85-hRkMn3qWftWDt-S3H3lW-QIyHrb0p6athF0HPonHj_hjjvW3J; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1541480148,1542068254,1542073540,1542096105; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1542096162''',
               'Host': 'index.baidu.com',
               'Referer': 'http://index.baidu.com/v2/main/index.html'}
    url = "http://index.baidu.com/api/SearchApi/index?word={}&area=0&days=30".format(quote(name))
    json_index = requests.get(url, headers=headers).json()
    # pprint(json_index)    # 用来观测json数据文件

    index_data = json_index["data"]
    # 判断是否是空值
    if len(index_data) != 0:
        index = index_data["generalRatio"][0]["all"]["avg"]
    else:
        index = 0
    return int(index)


def map_baidu_index(name):
    with open("./movie_info.csv", "a+", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if name != 0:
            print(datetime.now(), "{} enter ...".format(name))
            info = index_select(name)
            writer.writerow([name ,info])
            print(datetime.now(), "{} leave...".format(name))
        else:
            writer.writerow([0, 0])


if __name__ == "__main__":
    # a = index_select("金庸")
    # print(a)

    df = pd.read_csv("./movie_data/movie_info_lose_baiduindex.csv", encoding="utf-8")
    df.fillna({"direct":0, "actor":0}, inplace=True)
    direct = df["direct"]
    actor = df["actor"]


    with ThreadPool(4) as p:
        list(tqdm(p.imap(map_baidu_index, actor), total=len(direct)))








