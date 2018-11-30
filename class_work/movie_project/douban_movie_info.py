# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium import webdriver
from time import sleep, time
import csv
from pprint import pprint
import re
from tqdm import tqdm
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool


def douban_movie_url(movie_name):
    '''
    用无头浏览器渲染页面得到电影的URL
    :param movie_name: (String) 目标电影的名字(严格按照标准)
    :return: (String) 目标电影的url
    '''
    url = "https://movie.douban.com/subject_search?search_text={}&cat=1002".format(quote(movie_name))

    # 打开浏览器，并设置一系列设备
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")          # 设置headless浏览器
    options.add_argument("user-agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'")     # 设置UA
    prefs = { 'profile.default_content_setting_values': {'images': 2} }     # 不加载图片，省流量
    options.add_experimental_option('prefs', prefs)
    brower = webdriver.Chrome(options=options)

    # 浏览器渲染动态JS, 并提取电影独立的链接
    brower.get(url)
    brower.implicitly_wait(10)          # 最多等待10秒JS加载
    html = brower.page_source
    soup = BeautifulSoup(html, "html5lib")
    url = soup.find("a", href=re.compile("https://movie.douban.com/subject/"))["href"]
    sleep(0.5)          # 防止快速关闭，被认为爬虫
    brower.quit()
    return url


def douban_movie_info(url):
    '''
    提取电影页面主要信息
    :param url: (String) 电影的链接
    :return: (List) 电影的主要信息[导演，主演， 上映日期， 片长， 类型， 豆瓣评分， 评论数]
    '''
    info_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102' }
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html5lib")

    # 提取电影信息
    info_text = soup.find("div", id="info").get_text().strip()
    info_list.append([re.findall("导演: (.*?)\n", info_text)[0].split("/")[0]])
    info_list.append(re.findall("主演: (.*?) /", info_text))
    info_list.append(re.findall("上映日期: (\d+-\d+-\d+)", info_text))
    info_list.append(re.findall("片长: (\d+)分钟", info_text))
    info_list.append([re.findall("类型: (.*?)\n", info_text)[0].split("/")[0]])
    # 若没有匹配到信息，返回None
    info_list = [info[0] if len(info) else None for info in info_list]
    # 提取电影的评分和评价数
    try:
        rate = soup.find("strong", "ll rating_num", property="v:average").string
        comment_sum = soup.find("span", property="v:votes").string
    except AttributeError as e:
        rate, comment_sum = None, None
    info_list += [rate, comment_sum]

    return info_list


def movie_info_main(name):
    '''
    整合两个函数，方便直接调用
    :param name: (string) 电影名字
    :return: (list) 电影信息的列表
    '''
    url = douban_movie_url(name)
    sleep(np.random.randint(1,3))
    info = douban_movie_info(url)
    info.append(name)
    return info


def map_moie_info(name):
    '''纯业务，写入文本中去'''
    with open("./movie_all_info.csv", "a+", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        print(datetime.now(), "{} enter add func...".format(name))
        try:
            info = movie_info_main(name)
            writer.writerow(info)
            print(datetime.now(), "{} leave add func...".format(name))
        except:
            not_movie.append(name)
            print(name)
        finally:
            sleep(np.random.randint(0,2))



if __name__ == "__main__":

    # not_movie = []
    # lose = ['厉害了，我的国', '建党伟业', '建军大业', '建国大业']
    #
    # # info = douban_movie_info("https://movie.douban.com/subject/27605698/")
    # # print(info)
    # list(map(map_moie_info, lose))

    df = pd.read_csv("./movie_data/movie_money_info_USA.csv", encoding="utf-8", header=None)
    name_list = df.iloc[:,0]
    not_movie = []

    with ThreadPool(4) as p:
        r = list(tqdm(p.imap(map_moie_info, name_list), total=len(name_list)))

    print(not_movie)






