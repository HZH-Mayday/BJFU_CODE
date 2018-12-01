# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
from time import sleep
import csv
from urllib .parse import urlencode
from pprint import pprint
from tqdm import tqdm
from fake_useragent import UserAgent

user_agent = UserAgent()

Cookie = '''BAIDUID=C428230FAAA18689B8917B4C3EE6EFA0:FG=1; BIDUPSID=C428230FAAA18689B8917B4C3EE6EFA0; PSTM=1542168998; BDUSS=JHQ3VaZk5ubTBkOXNVUWpCSG5vTVQ0S1MzaE4tVFVVUXRsRXBIYzh3c24zaFJjQVFBQUFBJCQAAAAAAAAAAAEAAAACWfhUuf7C3nF3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACdR7VsnUe1bZX; pgv_pvi=6398349312; cflag=15%3A3; M_LG_UID=1425561858; M_LG_SALT=9709a87c8e394e037eb7db934e130360; validate=36368; MCITY=-131%3A'''

def forest_park_food_url_param(url, ):
    '''
    爬去一个公园的数据
    :param url: (String) 公园地图地址的url
    :return: (Dict) 包含公园周边商家的所有链接参数
    '''
    headers = {'User-Agent' : user_agent.random,
               'Host' : 'map.baidu.com',
               'Cookie' : Cookie}
    food_url_info = requests.get(url, headers=headers).json() # 读取页面的信息
    # pprint(food_url_info)
    food_auth = food_url_info["result"]["auth"]
    primary_uid = [ food_dict["primary_uid"] for food_dict in food_url_info["content"] ]
    uid = [food_dict["uid"] for food_dict in food_url_info["content"]]
    # 返回包含美食店面的链接参数
    return_dict = {"auth":food_auth, "primary_uid":primary_uid, "uid":uid}
    return return_dict


def food_info_get(auth, primary_uid, uid):
    '''
    提取百度页面中提示的店家信息(店名, 打分, 价格, 种类, 评价标签)
    :param auth: (String) 商家url中的参数
    :param primary_uid: (String) 商家url中的参数
    :param uid: (String) 商家url中的参数
    :return: (List) [店名, 打分, 价格, 种类, 评价标签]
    '''
    params = {"ugc_type":3, "ugc_ver":1, "qt":"detailConInfo", "device_ratio": 2, "compat":1,
            "t":1542697204078, "uid":uid, "primaryUid":primary_uid,"auth":auth}
    base_url = "https://map.baidu.com/?"
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
               'Cookie' : Cookie}
    food_json = requests.get(base_url, params=params, headers=headers).json()["content"]
    # pprint(json.loads(food_html))
    # 提取美食重要的信息
    price = food_json["ext"]["detail_info"].get("price", 0)
    rate = food_json["ext"]["detail_info"].get("overall_rating", 0)
    trade_tag = food_json["ext"]["detail_info"].get("trade_tag", None)
    comment_sum = food_json["ext"]["detail_info"].get("comment_num", 0)
    tag = food_json["showtag"]
    name = food_json["name"]
    return_list = [name, rate, price, tag, trade_tag, comment_sum]

    return return_list


def forest_park_food_info(url, ):
    '''
    整合两步操作, 写入文件
    :param url: 公园的url
    '''
    url_para = forest_park_food_url_param(url)
    sleep(2)

    # 把公园周边的美食信息全部爬取
    n = len(url_para["uid"])
    for i in range(n):
        try:
            food_info_list = food_info_get(url_para["auth"], url_para["primary_uid"][i], url_para["uid"][i])
        except TypeError as e:
            print("IP 被禁.....休息8秒")
            sleep(8)        # 太频繁可能被禁IP，休息8秒
            food_info_list = food_info_get(url_para["auth"], url_para["primary_uid"][i], url_para["uid"][i])
        with open("./food_info.csv", "a+" ,encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(food_info_list)
        # print(i, n)
        print( food_info_list )
        sleep(2)


if __name__ == "__main__":

    url = "https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c=131&wd=%E7%BE%8E%E9%A3%9F&wd2=&pn=0&nn=0&db=0&sug=0&addr=0&pl_data_type=cater&pl_sub_type=%E9%A4%90%E9%A6%86&pl_price_section=0%2C%2B&pl_sort_type=data_type&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=cater&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=16&uid=1d4bc84384a3c926eedfca70&r=1000&rn=50&tn=B_NORMAL_MAP&auth=AHgwDvTwMMVE8F4c9NWV%40BBRGvfebOG0uxHEzNLzBBEtxjhNwzWWvy1uVt1GgvPUDZYOYIZuxVtLlER1GD2dd9dv7uPWv3GuBVt%3DErpTgZp1GHJMP6V8%40aDcEWe1GD8zvOuiCbJXLwB19AhgW1GGDoEb1egvcguxHEzNxNzVEthl44yYxrZZWuV&u_loc=12952030,4828332&ie=utf-8&b=(12934763.2,4833651.13;12938247.2,4836543.13)&t=1542762335914"
    url1 = "https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c=131&wd=%E9%85%92%E5%BA%97&wd2=&pn=0&nn=0&db=0&sug=0&addr=0&pl_data_type=hotel&pl_sub_type=%E9%85%92%E5%BA%97&pl_price_section=0%2C%2B&pl_sort_type=default&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=hotel&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=16&rn=50&tn=B_NORMAL_MAP&auth=Ezb4PgCVbTVK%40PO6OICRS6%40MxXMCPYTWuxHEBHNRNRHt1qo6DF%3D%3DCy1uVt1GgvPUDZYOYIZuztFexLwWvcvY1SGpuHt300b0z8yPWv3GuHtYAmk5b7kzC1FILPRVX8ycEWe1GD8zvyu%3D95vyufvCu0iyfixA32135TATNwjnOOADzs99Xv7&u_loc=12952897,4826409&ie=utf-8&b=(12934769.2,4833897.13;12938241.2,4836789.13)&t=1543578785957"
    # url_para = forest_park_food_url_param(url)
    # print( len(url_para["uid"]) )
    # x = food_info_get(url_para["auth"], url_para["primary_uid"][11], url_para["uid"][11])
    # print(x)
    forest_park_food_info(url1)




