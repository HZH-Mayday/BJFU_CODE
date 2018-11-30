# -*- coding:utf-8 -*-
from urllib import request, parse
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from PIL import Image
import jieba
import numpy as np


def xiechen_comment(url, comment_page):
    '''
    爬取携程的评论
    :param url: (string) 爬虫链接
    :param comment_page: (int) 评论页数，从1开始
    :return: (list, int) 包含评论的列表, 评论的页数
    '''
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
              'host': "you.ctrip.com"}
    dict = {"poiID": 90851, "districtId": 0, "districtEName": "Beijing",
            "pagenow": comment_page, "order": 3.0, "star": 0.0, "tourist": 0.0,
            "resourceId": 107700, "resourcetype": 2}

    data = bytes(parse.urlencode(dict), encoding="utf-8")
    req = request.Request(url, data=data, headers=header, method="POST")
    response = request.urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(response, "html5lib")
    comment_list = [i.string for i in soup.find_all("span", "heightbox")]
    all_page = int(soup.find("b", "numpage").string)
    return comment_list, all_page



def draw_wordcloud(path, ):
    '''
    根据文本文档来制造词云
    :param path: (String) 文本文档的地址
    :return: 词云对象
    '''
    text = open(path, encoding='utf-8').read()
    # 结巴分词
    wordlist_after_jieba = jieba.cut(text, cut_all=False)
    wl_space_split = " ".join(wordlist_after_jieba)

    # 加载停用词
    stopwords_list = [line.strip() for line in open("D:/code_file/workspace/teacher_pa_work/xiechen_spyder/stopword_chinese.txt").readlines()]
    new_text = [word for word in wl_space_split.split(" ") if word not in stopwords_list and "一" not in word]
    new_string = ' '.join(new_text)
    # 创建词云对象
    font = 'C:\Windows\Fonts\simfang.ttf'  # 字体
    background = np.array(Image.open('D:/code_file/workspace/teacher_pa_work/xiechen_spyder/wordcloud_background.png'))
    word_cloud = WordCloud(collocations=False, font_path=font, width=2000, height=1400, margin=2,
                           random_state=42, background_color="white", mask=background).generate(new_string)
    # word_cloud.to_file('wordcloud/{}.png'.format(path[5:-4]))
    return word_cloud


if __name__ == "__main__":

    url = "http://you.ctrip.com/sight/beijing1/107700.html"
    comment, page = xiechen_comment(url, )
    print(page, comment)
    # x = draw_wordcloud("D:/code_file/workspace/class_work/data/爱情公寓.txt")
    # x.to_file("C:/Users/HuZheHui/Desktop/1.png")







