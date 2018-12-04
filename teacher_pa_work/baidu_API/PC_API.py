# -*- encoding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pprint import pprint
import re
from typing import List
from fake_useragent import UserAgent
use_agent = UserAgent()


def baidu_map_select(place : str) -> WebDriver:
    '''
    通过输入一个地方得到坐标位置的浏览器位置
    :param place: 地址
    :return: 返回地址左边位置的浏览器页面状态
    '''
    # 浏览器设置
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent='{}'".format(use_agent.random))
    prefs = { 'profile.default_content_setting_values': {'images': 2} }
    options.add_experimental_option('prefs', prefs)
    # options.add_argument('--headless')
    brower = webdriver.Chrome(options=options)
    brower.get("https://map.baidu.com/")

    # 进入森林公园，有多个地址
    forest_input = brower.find_element_by_id("sole-input")
    forest_input.send_keys(place)
    forest_input.send_keys(Keys.ENTER); sleep(1)

    return brower


def info_take_from(brower : WebDriver, tag : str) -> List[str]:
    '''
    提取附近内容的店面信息
    :param brower: 浏览器状态
    :param tag: 标签，例如：美食，住宿
    :return: 列表元素是 每个页面的信息
    '''
    # 点击第一个搜索结果，再点击附近，输入搜索内容
    brower.find_element_by_xpath('//*[@id="card-1"]/div/ul/li[1]').click(); sleep(1)
    brower.find_element_by_xpath('//*[@id="generalinfo"]/div[1]/div[1]').click(); sleep(1)
    around_input = brower.find_element_by_xpath('//*[@id="nearby-input"]')
    around_input.send_keys(tag)
    around_input.send_keys(Keys.ENTER); sleep(2)

    # 点击缩小页面布局
    # brower.find_element_by_xpath('//*[@id="map-operate"]/div[2]/div[2]/div[2]').click()
    # sleep(10)

    # 附近信息提取，还要点击页面提取下一个页面信息
    info = [brower.find_element_by_class_name('poilist').text]
    while True:
        if '米' in info[-1]:
            try:
                page_location = brower.find_element_by_xpath('//*[@id="poi_page"]/p')
                # 由于不同位置页面元素不同，选择最后一个页面按钮
                next_page = page_location.find_elements_by_tag_name('span')[-1]
                # 判断是否是最后一个页面按钮是否可以点击
                next_page_status = next_page.find_element_by_tag_name('a').get_attribute("onclick")
                if next_page_status is not None:
                    next_page.click(); sleep(2)
                    info.append(brower.find_element_by_class_name('poilist').text)
                else:
                    break
            except NoSuchElementException as e:
                break
        else:
            break

    brower.close()
    if len(info)==1 and '米' not in info[0]: info=[]
    return info


def deal_with_info(info : List[str]) -> List[str]:
    '''剔除1000m以外的页面信息'''
    shops_infos_list ,shop_info_list = [], []
    info_list = '\n'.join([i.strip() for i in info]).split('\n')
    for index, page_info in enumerate(info_list):
        shop_info_list.append(page_info)
        try:
            is_m = re.findall('^\d.*?米|\d.*?公里', info_list[index+1])
            if len(is_m)==1:
                shops_infos_list.append(shop_info_list)
                shop_info_list = []
        except IndexError as e:
            shops_infos_list.append(shop_info_list)

    # 去除1000米以外的店家数据
    m_km_shop_info = [','.join([_info.strip() for _info in shop_info]) for shop_info in shops_infos_list]
    m_shop_info_index = [m_km_shop_info[index] for index, shop_info in enumerate(m_km_shop_info) if '公里' not in shop_info]

    return m_shop_info_index



if __name__ == "__main__":

    brower = baidu_map_select("鹫峰国家森公园")
    info = info_take_from(brower, '公交车站')
    print(info)
    return_info = deal_with_info(info)

    for i in return_info:
        print(i)





