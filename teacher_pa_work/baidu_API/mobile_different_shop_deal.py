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


def get_next_page_info(select_infos, brower):
    '''
    提取一个页面的主要信息，并判断是否有下一页。若有，则提取页面信息
    :param select_infos: (function) 提取页面信息的函数
    :param brower: 浏览器状态
    :return: (list) 所有页面店家的信息
    '''
    shops_infos_list = select_infos(brower.page_source)
    if len(shops_infos_list)==0: return shops_infos_list
    while True:
        try:
            next_page = brower.find_element_by_xpath('//*[@id="fis_elm_pager__qk_6"]/div/div/span[2]')
            next_page_status = next_page.get_attribute("class").strip()
            # 有些页面1000m内没有店家，就返回全部，这时候要与下一页分别
            is_1000km = sum(['km' in i for i in shops_infos_list[-1]])
            if next_page_status == "page-btn" and is_1000km == 0:
                next_page.click();  sleep(1)
                shops_infos_list += select_infos(brower.page_source)
            else:
                break
        except NoSuchElementException:
            break
    return shops_infos_list


def food_around(brower, tag="餐饮"):
    # 进入森林公园周边搜索页面，并输入关键字
    wait = UI.WebDriverWait(brower, 10)
    cate = brower.find_element_by_id("search-input")
    cate.send_keys(tag)
    cate.send_keys(Keys.ENTER); sleep(1)

    # 点击筛选目录，确认在1000米内的商家
    brower.find_element_by_xpath('//*[@id="cater-filter"]/menu/li[1]/a').click(); sleep(1)
    brower.find_element_by_xpath('//*[@id="filter-container"]/div[2]/div/menu[2]/ul/li[3]').click(); sleep(1)

    # 提取当前页面店家的有效信息，并对有下一页的店家页面信息进行提取
    shops_infos_list = get_next_page_info(select_food_infos, brower)
    brower.close()
    return shops_infos_list


def select_food_infos(page_source):
    shops_infos_list= []
    soup = BeautifulSoup(page_source, "html5lib")
    shops_infos = soup.find_all("li", attrs={"data-url": re.compile("/mobile/webapp/place/detail/")})
    for shop_info in shops_infos:
        print(shop_info.text)
        name = shop_info.find("span", "text-ellipsis list-tit-con").string
        type = shop_info.find("div", "item-tag text-ellipsis").string.strip().split("\n")[0]
        dis = shop_info.find("em", "list-dis-img").string
        rate_list = re.findall("\n(\d\.\d)", shop_info.text)
        rate = rate_list[0] if len(rate_list) != 0 else 0
        price_list = re.findall("¥(.*?)\n", shop_info.text)
        price = price_list[0] if len(price_list) != 0 else 0
        result_tag = [name, rate, type, dis, price]
        shops_infos_list.append(result_tag)
    return shops_infos_list



def serves_around(brower, serves_tag="超市"):
    # 进入森林公园周边搜索页面，并输入关键字
    wait = UI.WebDriverWait(brower, 10)
    cate = brower.find_element_by_id("search-input")
    cate.send_keys(serves_tag)
    cate.send_keys(Keys.ENTER); sleep(1)

    # 点击筛选目录，确认在1000米内的商家
    brower.find_element_by_xpath('//*[@id="dist"]/span/i').click(); sleep(1)
    brower.find_element_by_xpath('//*[@id="fis_elm_pager__qk_4"]/div/div[2]/div/div[2]/ul/li[3]').click(); sleep(1)

    # 提取当前页面店家的有效信息，并对有下一页的店家页面信息进行提取
    shops_infos_list = get_next_page_info(select_serves_infos, brower)
    brower.close()
    return shops_infos_list

def select_serves_infos(page_source):
    serves_infos_list = []
    soup = BeautifulSoup(page_source, "html5lib")
    serves_infos = soup.find_all("a", attrs={"href": re.compile("/mobile/webapp/place/detail/")})
    for serves_info in serves_infos:
        dis = serves_info.find("span", "dis -col-auto").string
        if "km" in dis: break
        name = serves_info.find("h4", "text-ellipsis -ft-primary -ft-large").string
        serves_infos_list.append([name, dis])
    return serves_infos_list



def hotail_around(brower, serves_tag="酒店"):
    # 进入森林公园周边搜索页面，并输入关键字
    wait = UI.WebDriverWait(brower, 10)
    cate = brower.find_element_by_id("search-input")
    cate.send_keys(serves_tag)
    cate.send_keys(Keys.ENTER); sleep(1)

    # 点击筛选目录，确认在1000米内的商家
    brower.find_element_by_xpath('//*[@id="fis_elm_pager__qk_6"]/div[2]/ul/li[2]').click(); sleep(1)

    # 提取当前页面店家的有效信息，并对有下一页的店家页面信息进行提取
    shops_infos_list = get_next_page_info(select_serves_infos, brower)
    brower.close()
    return shops_infos_list

def select_hotail_infos(page_source):
    serves_infos_list = []
    soup = BeautifulSoup(page_source, "html5lib")
    serves_infos = soup.find_all("li", attrs={"data-url": re.compile("/mobile/webapp/place/detail/")})
    for serves_info in serves_infos:
        dis = serves_info.find('span', 'dis-num').string[2:]
        if "km" in dis: break
        name = serves_info.find('span', 'list-tit text-ellipsis tit-len1').string
        rate = serves_info.find('span', 'star-num').string[:-1]
        price = serves_info.find('span', 'price-num').string.strip()
        serves_infos_list.append([name, rate, price, dis])
    return serves_infos_list



