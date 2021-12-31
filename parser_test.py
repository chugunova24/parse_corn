import datetime
import sched, time
from babel.dates import format_date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

import threading
from babel.dates import format_date, format_datetime
from pprint import pprint
import asyncio
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from lxml import etree
import re

start_time = time.time()

# работа браузера без интерфейса
option = Options()
option.headless = False

# # chrome_options = webdriver.ChromeOptions()
# PROXY = "103.124.2.229:3128"
# option.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(options=option)
driver.set_window_size(1920, 1080)

x = datetime.datetime.today()
x2 = datetime.datetime.date(x)
date_today = format_date(x2, locale='de_DE')

def nasdaq_com():
    URL = '''https://www.nasdaq.com/news-and-insights/topic/markets/commodities'''
    xPATH = '''//a[@class="content-feed__card-title-link"]'''
    xPATH_link = '''//a[@class="content-feed__card-title-link"]/@href'''
    xPATH_element = '''/html/body/div[1]/div/main/div[2]/div[2]/div/div[1]/section/div[1]/div/div[2]/div/div[1]/div'''

    #  -------------- BS4 ----------------

    # webpage = requests.get(URL, timeout=10)
    # print('страница получена')
    # soup = BeautifulSoup(webpage.content, "html.parser")
    # print('страница получена2')
    # dom = etree.HTML(str(soup))
    # print('дом')
    # count_index = dom.xpath(xPATH)
    # print('дом поиск икспаф')
    #
    # # поиск содержимого блоков НА 1 СТРАНИЦЕ
    # cell_news_arr = []
    # for i in range(0, len(count_index)):
    #     a = dom.xpath(xPATH)[i].text
    #     print('получить текст из элементов')
    #     cell_news_arr.append(a)
    # print(cell_news_arr)
    #
    # # # поиск ссылок на содержимое блоков
    # # news_link_arr = []
    # # for i in range(0, len(count_index)):
    # #     a = dom.xpath(xPATH_link)[i]
    # #     news_link_arr.append(a)


    try:
        driver.get(URL)
        # driver.execute_script("window.stop();")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xPATH_element)))
        print('window STOP')
        # ищет новости на сегодня
        cell_news_arr = []
        cell_news = driver.find_elements(By.XPATH, xPATH)
        for i in cell_news:
            cell_news_arr.append(i.text)
        print(cell_news_arr)

    finally:
        driver.quit()

    # # ищет новости на сегодня
    # cell_news_arr = []
    # cell_news = driver.find_elements(By.XPATH, xPATH)
    # for i in cell_news:
    #     cell_news_arr.append(i.text)
    # print(cell_news_arr)


nasdaq_com()

print("--- %s seconds ---" % (time.time() - start_time))