# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as UI
from time import sleep
from pprint import pprint
from fake_useragent import UserAgent

from mobile_different_shop_deal import food_around, serves_around, hotail_around


user_agent = UserAgent()

def get_forest_url(forest_park):
    # 浏览器设置
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent='{}'".format(user_agent.random))
    # options.add_argument("--headless")
    prefs = {'profile.default_content_setting_values': {'images': 2}}
    options.add_experimental_option('prefs', prefs)
    brower = webdriver.Chrome(options=options)
    wait = UI.WebDriverWait(brower, 10)
    brower.get("https://map.baidu.com/mobile/webapp/index"); sleep(1)
    # 进入森林公园，选择森林公园的链接
    forest_input = brower.find_element_by_id("se-input-poi")
    forest_input.send_keys(forest_park)
    forest_input.send_keys(Keys.ENTER)
    # 等待页面加载，太快会导致页面节点无法出现报错
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="list-container"]/ul/li[1]/ul/li[2]')))
    # 返回森林公园周边搜索的链接，并打开页面
    page_source = brower.page_source
    soup = BeautifulSoup(page_source, "html5lib")
    base_url = soup.find("ul", "features").find("li", attrs={"data-type":"near"})["data-href"]
    forest_url = "https://map.baidu.com{}".format(base_url)
    brower.get(forest_url)

    return brower



if __name__ == "__main__":
    b = get_forest_url("北京西山国家森林公园")
    y = serves_around(b, "厕所")
    print(y)
    # x =  hotail_around(b)
    # print(x)

    # # 得到森林公园的详情链接
    # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="list-container"]/ul/li[1]/div')))
    # page_source = brower.page_source
    # soup = BeautifulSoup(page_source, "html5lib")
    # base_url = soup.find("div", "info")["data-url"]
    # forest_url = "https://map.baidu.com{}".format(base_url)

