# -*- encoding:utf-8 -*-
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as UI
from time import sleep
from pprint import pprint

def baidu_map_select(url):
    # 浏览器设置
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36'")
    prefs = { 'profile.default_content_setting_values': {'images': 2} }
    options.add_experimental_option('prefs', prefs)
    brower = webdriver.Chrome(options=options)
    wait = UI.WebDriverWait(brower, 10)
    brower.get(url)

    # 进入森林公园，有多个地址
    forest_input = brower.find_element_by_id("sole-input")
    forest_input.send_keys("北京西山国家森林公园")
    forest_input.send_keys(Keys.ENTER)
    print("休息5秒钟.....")
    sleep(5)

    soup = BeautifulSoup(brower.page_source, "html5lib")
    pprint(soup)
    # print("开始目标测试")
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-item scenery-item")))
    # right_click = brower.find_element_by_class_name("search-item scenery-item")
    # print(right_click)

    # ActionChains(brower).context_click(right_click).perform()
    # # 进入第一个地址的附近
    # forest_butten = brower.find_element_by_xpath('//*[@id="generalinfo"]/div[1]/div[1]/span[1]')
    # forest_butten.click()
    #
    # forest_food_input = brower.find_element_by_xpath('//*[@id="nearby-input"]')
    # forest_food_input.send_keys("美食")
    # forest_food_input.send_keys(Keys.ENTER)
    brower.close()




if __name__ == "__main__":
    baidu_map_select("https://map.baidu.com/")


