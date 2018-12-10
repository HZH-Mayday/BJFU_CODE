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
    info_list = re.findall('\d+\s*\..*?m', info_list, re.S)
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
    print(text_list)
    info = deal_with_text(text_list, distance)
    return info



if __name__ == "__main__":

    x = main("西山国家森林公园", "厕所", 5)
    # y = ['1 .肯德基(八达岭餐厅)\n3.0 / 5.0\n人均： ¥33.0\n西式快餐 八达岭\n2.1km\n停车不方便 店面较大 上菜较慢\n2 .长城山林农家院\n5.0 / 5.0\n中餐馆\n1.2km\n空间小 卫生干净 吃得不错\n3 .姬家老店\n2.7 / 5.0\n人均： ¥93.0\n中餐馆\n1.2km\n4 .庆丰包子铺(八达岭长城店)\n3.3 / 5.0\n人均： ¥30.0\n包子 八达岭\n2.3km\n环境不错\n5 .八达岭饭店\n3.3 / 5.0 wifi parking\n人均： ¥50.0\n中餐馆\n2km\n味道一般 菜品较少 消费偏高\n6 .李先生(八达岭长城店)\n5.0 / 5.0\n人均： ¥19.0\n中式快餐 八达岭\n2.3km\n7 .赛百味(八达岭长城店)\n3.9 / 5.0 wifi parking\n人均： ¥36.0\n西式快餐 八达岭\n2.2km\n份量很足\n8 .万里长城·八达岭外宾餐厅\n3.0 / 5.0\n中餐馆\n1.7km\n9 .八达岭长城饭店-中餐厅\n3.2 / 5.0\n中餐馆\n2.2km\n10 .飞飞居农家饭\n4.7 / 5.0\n人均： ¥58.0\n中餐馆 八达岭\n4km\n老店 位置较偏 现点现做\n上一页 下一页', '1 .八达岭鸿福老北京炸酱面店\n3.5 / 5.0\n人均： ¥44.0\n粉面馆\n2.2km\n环境一般 消费偏高 服务一般\n2 .长城胡家老店农家院\n2.5 / 5.0\n中餐馆 八达岭\n3km\n价格贵 环境好\n3 .岔道古驿(岔道村店)\n5.0 / 5.0\n中餐馆 八达岭\n4.2km\n4 .铁锅王农家餐厅\n2.8 / 5.0\n人均： ¥40.0\n中餐馆 八达岭\n3.4km\n5 .长城天地美食文化广场\n4.2 / 5.0\n人均： ¥45.0\n中餐馆 八达岭\n3.9km\n菜品丰富 味道不错\n6 .公社山景餐厅\n2.8 / 5.0 wifi parking\n人均： ¥500.0\n西餐厅\n2.2km\n服务很好 味道不错\n7 .稻香村(延庆县八达岭长城店)\n5.0 / 5.0\n蛋糕甜点\n2.2km\n老字号\n8 .宇泰\n5.0 / 5.0\n商铺\n2.2km\n9 .鲜果时间(熊乐园店)\n2.6 / 5.0\n蛋糕甜点\n1.4km\n东西贵 知名品牌 人很多\n10 .阿泰包子(八达岭店)\n0.0 / 5.0\n人均： ¥14.0\n包子\n1.4km\n菜品较少 份量很足 服务很好\n上一页 下一页', '1 .八达岭饭店西餐厅\n3.4 / 5.0\n西餐厅\n2km\n2 .八达岭森林公园餐厅\n0.0 / 5.0\n中餐馆\n904m\n3 .北京特产稻香村糕点全聚德烤鸭\n北京菜\n2.2km\n4 .大笨锅乡村铁锅炖\n4.3 / 5.0\n人均： ¥77.0\n中餐馆 八达岭\n4.9km\n停车不方便 人气旺 份量很足\n5 .山西面馆\n粉面馆 八达岭\n2.2km\n6 .延庆八达岭邵家大院\n4.8 / 5.0\n人均： ¥99.0\n八达岭 经济型 八达岭\n3.5km\n7 .庄户人家民俗饭庄(延庆店)\n2.0 / 5.0 wifi parking\n人均： ¥100.0\n中餐馆 八达岭\n3.7km\n8 .北京八达岭长城天地餐饮有限责任公司\n公司\n894m\n9 .王家大院(岔道路)\n2.1 / 5.0\n中餐馆 八达岭\n3.8km\n10 .青龙泉休闲度假村餐厅\n838m\n上一页 下一页', '1 .拾间房\n4.0 / 5.0\n中餐馆\n2km\n2 .八达岭夏都兰州牛肉拉面\n0.5 / 5.0\n人均： ¥22.0\n粉面馆 八达岭\n2.3km\n环境一般 消费偏高 份量较小\n3 .富强农家院6号\n2.0 / 5.0\n人均： ¥46.0\n农家院\n2.2km\n4 .双静苑咖啡厅\n0.0 / 5.0\n咖啡厅 八达岭\n2.2km\n5 .老北京炸酱面(延庆店)\n粉面馆 八达岭\n2.3km\n6 .黄焖鸡米饭\n中式快餐 八达岭\n2.1km\n7 .观景阁餐厅\n4.0 / 5.0\n中餐馆\n2.6km\n环境不错\n8 .刘家老店(岔道路)\n2.7 / 5.0\n中餐馆 八达岭\n3.8km\n隔音不好 卫生一般 饭菜一般\n9 .天津包子\n包子 八达岭\n2.3km\n10 .久久丫鸭脖\n熟食\n1.4km\n上一页 下一页', '1 .石门酒吧\n0.5 / 5.0\n酒吧\n2.3km\n2 .古长城餐厅\n3.0 / 5.0\n中餐馆\n3.5km\n位置好找 菜品丰富 服务很好\n3 .迎宾饭店\n0.5 / 5.0\n中餐馆 八达岭\n2.3km\n位置较偏 人不多 环境一般\n4 .延吉冷面\n粉面馆 八达岭\n2.1km\n5 .八达岭车站快餐\n快餐 八达岭\n2.8km\n6 .牛街小吃\n0.5 / 5.0\n人均： ¥50.0\n小吃 八达岭\n3.9km\n价格实惠 服务很好\n7 .北京烤鸭\n北京菜\n2.3km\n8 .北京岔道农家院\n1.0 / 5.0\n北京菜\n3.9km\n9 .Butik & Akta Kaffe\n咖啡厅\n1.9km\n10 .老北京云鹰饭馆\n北京菜\n2km\n上一页 下一页', '1 .内蒙烤肉\n烧烤\n2.2km\n2 .老坛酸菜面\n粉面馆 八达岭\n2.1km\n3 .硒空间\n4.0 / 5.0\n快餐 八达岭\n3.9km\n交通方便 环境不错 服务很好\n4 .现磨咖啡\n咖啡厅 八达岭\n2.1km\n5 .清真兰州拉面\n粉面馆 八达岭\n3.9km\n6 .正宗兰州拉面\n0.0 / 5.0\n粉面馆\n2.2km\n7 .家味老北京炸酱面\n0.0 / 5.0\n粉面馆 八达岭\n2.1km\n8 .合和园农家菜(水关长城店)\n餐馆\n2.1km\n9 .咖啡屋茶\n0.0 / 5.0\n咖啡厅\n2.2km\n10 .爱米粉\n0.2 / 5.0\n粉面馆 八达岭\n2.2km\n上一页 下一页', '1 .优力克汉堡\n汉堡 八达岭\n2.2km\n2 .河间驴肉火烧\n人均： ¥17.0\n小吃 八达岭\n2.2km\n3 .实惠小吃\n小吃 八达岭\n2.2km\n4 .好汉坡咖啡\n0.0 / 5.0\n咖啡厅\n2.2km\n5 .手抓饼小笼包烤玉米汉堡\n汉堡\n2.2km\n6 .成都小吃川湘菜\n0.0 / 5.0\n中餐馆\n2.2km\n7 .家和豆浆\n快餐\n2.2km\n8 .渔家鲜\n中餐馆 八达岭\n3.3km\n9 .八达岭农家炒菜馆\n中餐馆 八达岭\n2.3km\n10 .正新鸡排\n快餐\n2.3km\n上一页 下一页', '1 .遇见名小吃\n小吃 八达岭\n2.3km\n2 .四桥餐馆\n2.0 / 5.0\n中餐馆\n4.6km\n3 .北京面馆\n粉面馆 八达岭\n3.9km\n4 .晶晶餐馆\n中餐馆 八达岭\n2.8km\n5 .鸵鸟园\n餐馆\n2.9km\n6 .田园农家\n中餐馆 八达岭\n3.2km\n7 .陕西风味\n人均： ¥49.0\n中餐馆 八达岭\n3.9km\n8 .乐游自助餐\n0.0 / 5.0\n自助餐 八达岭\n3.9km\n9 .北京同福缘客寨\n0.0 / 5.0\n北京菜 八达岭\n3.6km\n10 .北京八达岭岔道刘建永农家院餐厅\n0.0 / 5.0\n人均： ¥0.0\n八达岭 中餐馆 八达岭\n3.6km\n上一页 下一页', '1 .康秀花特色民宿\n八达岭\n3.6km\n2 .好越来小院北方特色农家乐\n3.9km\n3 .湖南蒸菜\n人均： ¥15.0\n中餐馆 八达岭\n3.9km\n上一页 下一页']
    # x = deal_with_text(y)
    # print(x)











