# -*- coding:utf-8 -*-
import sys
sys.path.append("../../")
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
from draw_set import seaborn_set
seaborn_set()
from pprint import pprint

def meituan_spyder(url, ):
    '''
    读取美团的评价的打分和评论
    :param url: (String) 美团评价的链接
    :return: (dict) 包含三个元素， 打分(list)， 评论(list)， 标签数量(DataFrame)
    '''
    return_dict = {"star":[], "comment":[], "tag_count_df":None }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102',}
    html = requests.get(url, headers=headers).text  # 读取页面的信息
    all_info = BeautifulSoup(html, 'html5lib').find("body").string
    info_dict = json.loads(all_info)

    # 提取打分和评论
    comments = info_dict["comments"]
    for pearson in comments:
        star = pearson["star"]
        comment = pearson["comment"]
        return_dict["star"].append(star)
        return_dict["comment"].append(comment)

    # 提取标签和文字
    tag_count = np.array([[d["count"], d["tag"]] for d in info_dict["tags"]])
    tag_count_df = pd.DataFrame(tag_count, columns=["count", "tag"])
    return_dict["tag_count_df"] = tag_count_df

    # 评论信息读取
    return return_dict

if __name__ == "__main__":

    url="https://www.meituan.com/ptapi/poi/getcomment?id=1679122&offset=0&pageSize=10&mode=0&sortType=1"
    return_dict = meituan_spyder(url)
    df = return_dict["tag_count_df"]
    df["count"] = df["count"].apply(np.int)

    print(df)
    # # 对标签数据进行可视化处理
    # fig, ax = plt.subplots()
    # df.plot(kind="barh", x="tag", y="count", ax=ax)
    # ax.set(title="标签的条形统计图", xlabel="评论标签", ylabel="评论人数", xlim=[0,400])
    # ax.legend().set_visible(False)
    # plt.show()






