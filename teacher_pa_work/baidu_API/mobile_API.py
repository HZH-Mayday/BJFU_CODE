# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from time import sleep
from fake_useragent import UserAgent
from typing import List

user_agent = UserAgent()

def forest_park_input(forest_park : str) -> WebDriver:
    '''
    :param forest_park: 目标地址
    :return: 返回输入目标地址后，进入周边搜索的页面信息
    '''
    # 浏览器设置
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent='{}'".format(user_agent.random))
    # options.add_argument("--headless")
    prefs = {'profile.default_content_setting_values': {'images': 2}}
    options.add_experimental_option('prefs', prefs)
    brower = webdriver.Chrome(options=options)
    brower.get("https://map.baidu.com/mobile/webapp/index"); sleep(1)
    # 进入森林公园，选择森林公园的链接
    forest_input = brower.find_element_by_id("se-input-poi")
    forest_input.send_keys(forest_park)
    forest_input.send_keys(Keys.ENTER); sleep(2)

    # 点击地点进入目标的详情页面
    try:
        brower.find_element_by_xpath('//*[@id="list-container"]/ul/li[1]').click(); sleep(2)
    except NoSuchElementException:
        brower.find_element_by_xpath('//*[@id="fis_elm_pager__qk_6"]/div/ul/li[1]').click(); sleep(2)
    # 点击详情页面的周边按钮
    brower.find_element_by_xpath('//*[@id="phoenix-header"]/div[3]/a[1]').click(); sleep(2)
    return brower


def forest_park_around(brower : WebDriver, tag : str ="超市", distance : int =5) -> List[str]:
    '''
    输入搜索周边的内容，筛选目标范围内的店铺信息列表(包括翻页后的信息)
    :param brower: 进入搜素周边页面信息
    :param tag: 搜索周边的内容
    :param distance: 筛选5km以内的店铺(参数值5不做改变)
    :return: 全部店铺信息列表
    '''
    # 进入森林公园周边搜索页面，并输入关键字
    cate = brower.find_element_by_id("search-input")
    cate.send_keys(tag)
    cate.send_keys(Keys.ENTER); sleep(2)

    # 点击筛选目录，确认在5000米内的商家
    # 一般三种分类模式，吃的，住的，服务类
    try:
        brower.find_element_by_xpath('//*[@id="dist"]/span/i').click(); sleep(1)
        brower.find_element_by_xpath('//*[@id="fis_elm_pager__qk_4"]/div/div[2]/div/div[2]/ul/li[5]').click(); sleep(2)
        text_id = 7
    except NoSuchElementException:
        try:
            brower.find_element_by_xpath('//*[@id="cater-filter"]/menu/li[1]').click(); sleep(1)
            brower.find_element_by_xpath('//*[@id="filter-container"]/div[2]/div/menu[2]/ul/li[5]').click(); sleep(2)
            text_id = 6
        except NoSuchElementException:
            brower.find_element_by_xpath('//*[@id="fis_elm_pager__qk_6"]/div[2]/ul/li[2]').click(); sleep(1)
            text_id = 7

    # 点击目标范围内的全部页面，提取所有信息
    text_list = []
    while True:
        try:
            # 把当前页面的信息全部提取
            text = brower.find_element_by_xpath('//*[@id="fis_elm_pager__qk_{}"]/div'.format(text_id)).text
            text_list.append(text)
            # 出现目标公里以外的数据,直接跳出循环
            if sum(['{}.{}km'.format(distance, i) in text for i in range(1,10)]) != 0:
                break
            # 找到下一页的按钮，并点击页面
            next_page = brower.find_element_by_xpath('//*[@id="fis_elm_pager__qk_{}"]/div/div/span[2]'.format(text_id))
            next_page_status = next_page.get_attribute("class").strip()
            if next_page_status == "page-btn":
                next_page.click();  sleep(2)
            else:
                print("没有下一页")
                break
        # 若没有下一页按钮，直接退出循环
        except NoSuchElementException:
            print("没找到元素")
            break

    brower.close()
    return text_list


def deal_with_text(text_list : List[str], distance : int =5) -> List[str]:
    '''
    对杂乱的文档内容进行整理，主要是单个商家作为一个元素
    剔除目标范围外的店家
    :param text_list: 原始每个页面的店铺信息
    :param distance: 目标距离
    :return: [每一个目标范围店铺信息, ]
    '''
    info_list = '\n'.join([text.strip() for text in text_list])
    info_list = re.findall('\d+\..*?m', info_list, re.S)
    info_list = [i.replace('\n', ' ') for i in info_list]

    # 得到小于目标距离的数据指标
    dis_km_inner_index= []
    for index, info in enumerate(info_list):
        dis = re.findall("(\d\.*\d*)km", info)
        if len(dis) == 0 or float(dis[0]) <= distance:
            dis_km_inner_index.append(index)
    dis_km_inner_info = [info_list[i] for i in dis_km_inner_index]

    return dis_km_inner_info


def main(forest_park, around_tag, distance=5):
    brower = forest_park_input(forest_park)
    print("进入周边搜索页面....")
    text_list = forest_park_around(brower, around_tag)
    print("存储所有目标店铺的信息")
    info = deal_with_text(text_list, distance)
    return info



if __name__ == "__main__":

    x = main("八达岭森林公园", "医院", 5)
    for i in x: print(i)












