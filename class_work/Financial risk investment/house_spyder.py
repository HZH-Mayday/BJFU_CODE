# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from pprint import pprint
from typing import List
import csv
import re
from time import sleep
from tqdm import tqdm
from multiprocessing.dummy import Pool

Use_Agent = UserAgent()

def woaiwojia_spyder(page : int) -> List[list]:
    '''
    爬取我爱我家二手房的数据
    :param page: (int) 页面数据
    :return: (list) 二手房的数据
    '''
    info_list = []
    url = 'https://bj.5i5j.com/ershoufang/n{}/'.format(page)
    headers = {'User-Agent' : Use_Agent.random}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html5lib')
    # pprint(soup)
    # 方便用正则表达式读取
    all_house_information = [','.join([str(p) for p in f.find_all('p')]) for f in  soup.find_all('div', 'listX')]
    # 读取每一个房子的信息， 没有读取到的目标信息（默认：None）
    for one_house_info in all_house_information:
        # 用正则表达式读取
        room = re.findall('(\d+)室', one_house_info)
        hall = re.findall('(\d+)厅', one_house_info)
        bathroom = re.findall('(\d+)卫', one_house_info)
        size = re.findall('·(.*?)平米', one_house_info)
        floor = re.findall('/(\d+)层', one_house_info)
        distance = re.findall('距离地铁.*?(\d+)米', one_house_info)
        watch = re.findall('</i>(\d+)  人关注', one_house_info)
        visit = re.findall('近30天带看  (\d+)  次', one_house_info)
        price = re.findall('<strong>(\d+)', one_house_info)
        unit_price = re.findall('单价(\d+)', one_house_info)
        house_info_list = [room, hall, bathroom, size, floor, distance, watch, visit, unit_price, price]
        house_info_list = [float(i[0]) if len(i) != 0 else None for i in house_info_list]
        info_list.append(house_info_list)

    return info_list


def writer(page : int) -> None:
    with open('./house1.csv', 'a+', newline="", encoding="utf-8") as csvfile:
        input_list = woaiwojia_spyder(page)
        if len(input_list) != 0:
            writer = csv.writer(csvfile)
            writer.writerows(input_list)
            sleep(2)
        else:
            print("page {} is not success...".format(page))
            not_success_page.append(page)

if __name__ == "__main__":

    # x = woaiwojia_spyder(1)
    # print(x)

    not_success_page = []
    with Pool(4) as p:
        list(tqdm(p.imap(writer, list(range(101,401))), total=300))
    print(not_success_page)


