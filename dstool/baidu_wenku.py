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



def baidu_wenku(url):
    '''
    用无头浏览器渲染页面得到电影的URL
    :param movie_name: (String) 目标电影的名字(严格按照标准)
    :return: (String) 目标电影的url
    '''

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
    ele_text = soup.find_all("p", "p-txt", style="font-size: 14px; line-height: 1.4;")
    text = [ele.string for ele in ele_text]
    brower.quit()
    return text

if __name__ == "__main__":

    x = baidu_wenku("https://wenku.baidu.com/view/60287b2e0a4e767f5acfa1c7aa00b52acfc79ccf.html")
    print(x)
    with open("11.txt", "w+", encoding="utf-8") as f:
        for t in x:
            if t is not None:
                f.write(t)


