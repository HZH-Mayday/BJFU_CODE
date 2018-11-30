# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import json
import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from pprint import pprint

def from_movie_name_to_money(movie_name):
    '''
    通过电影的名字返回电影的票房，电影的名字要准确(参考cbooo.cn)
    :param movie_name: (String) 电影的名字
    :return: (float) 电影的票房
    '''
    # 通过电影的名字获取电影的主页面
    url = "http://www.cbooo.cn/search?k={}".format(quote(movie_name))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102', }
    url_html = requests.get(url, headers=headers).text
    url_soup = BeautifulSoup(url_html, "html5lib")
    try:
        movie_url = url_soup.find("a", target="_blank", href=re.compile("http://www.cbooo.cn/m/"))["href"]
    except TypeError as e:
        print("电影名称输入有误，请输入电影全称")
        return
    # 通过主页面获取电影的票房
    return movie_url


def movie_money_return(url):
    '''
    根据电影的链接提取出对应的票房
    :param url: (String) 电影的链接
    :return: (Float) 电影的票房
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102',}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html5lib")
    money_tag = soup.find("span", "m-span")
    # 用正则提取出对应的票房
    if money_tag is not None:
        money_patten = re.compile("(\d+.*?)万")
        money = float(re.findall(money_patten, str(money_tag))[0])
    else:
        print("电影名字输入不够准确，没有对应的票房")
        money = None
    return money


def movie_money_main(name):
    movie_url = from_movie_name_to_money(name)
    if movie_url is not None:
        sleep(np.random.randint(0,3))
        print(movie_url)
        money = movie_money_return(movie_url)
        return money
    else:
        return


if __name__ == "__main__":
    x = movie_money_main("大圣归来")
    print(x)
