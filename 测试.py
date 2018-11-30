# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pprint import pprint
import requests

# browser = webdriver.Chrome()
# try:
#     browser.get("https://www.baidu.com/")
#     input = browser.find_element_by_id("kw")
#     input.send_keys("Python")
#     input.send_keys(Keys.ENTER)
#     wait = WebDriverWait(browser, 10)
#     wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
#     print(browser.current_url)
#     print(browser.get_cookies())
#     print(browser.page_source)
# finally:
#     browser.close()


browser = webdriver.Chrome()
browser.get("http://www.dianping.com/shop/9018161")
pprint(browser.page_source)
browser.close()

# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36'}
# x = requests.get("http://echarts.baidu.com/examples/editor.html?c=bar-negative", headers=headers)
# print(x.text)


