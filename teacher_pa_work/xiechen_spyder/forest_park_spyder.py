# -*- coding:utf-8 -*-
import os
current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
file_path = father_path.replace("\\","/")
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import jieba
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image


def reload_comment(url, cookie):
    '''
    读取携程网上的评论信息
    :param url: (string)
    :return: (list) 返回一个页面的评论信息
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102',
               'Cookie': cookie}
    html = requests.get(url, headers=headers).text      # 读取页面的信息
    soup = BeautifulSoup(html, 'lxml')
    # 评论信息读取
    text = soup.find_all("span", "heightbox")
    text_comment = [t.string for t in text]
    return text_comment


def writer_text(place, text_comment):
    '''
    把数据写入文档
    :param place: (sting) 森林公园
    :param text_comment: (String) 评论列表
    '''
    with open("data/{}.txt".format(place), "wt", newline='', encoding='utf-8') as t:
        for text in text_comment:
            t.write(text)


def draw_cloud(path, ):
    text = open(path, encoding='utf-8').read()
    # 结巴分词
    wordlist_after_jieba = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist_after_jieba)
    # 加载停用词
    stopwords_list = [line.strip() for line in open(file_path+"/stopword_chinese.txt").readlines()]
    new_text = [word for word in wl_space_split.split(" ") if word not in stopwords_list and "一" not in word]
    new_string = ' '.join(new_text)
    # 创建词云对象
    font = 'C:\Windows\Fonts\simfang.ttf'       # 字体
    background = np.array(Image.open(file_path+'/wordcloud_background.png'))
    word_cloud = WordCloud(collocations=False, font_path=font, width=2000, height=1400, margin=2,
                            random_state=42, background_color="white", mask=background).generate(new_string)
    word_cloud.to_file('wordcloud/{}.png'.format(path[5:-4]))


if __name__ == "__main__":

    df = pd.read_excel("url.xls", encoding="utf-8")
    df.drop_duplicates("place", inplace=True)

    # for i in range(len(df)):
    #     url = df.iloc[i, 1]
    #     cookie = df.iloc[i, 2]
    #     text = reload_comment(url, cookie)
    #     print(text)
    #     writer_text(df.iloc[i,0], text)

    for place in df["place"]:
        draw_cloud("data/{}.txt".format(place))
        print(place)





