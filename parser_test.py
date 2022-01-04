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
option.headless = True

# chrome_options = webdriver.ChromeOptions()
# # # PROXY = "8.210.149.254:59394"
# PROXY = "8.210.149.254:59394"
# option.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(options=option)
driver.set_window_size(1920, 1080)

x = datetime.datetime.today()
x2 = datetime.datetime.date(x)
date_today = format_date(x2, locale='de_DE')

def forbes_ru():
    # date_today = '03.12.2021'

    URL = 'https://www.forbes.ru/'
    xPATH = '''//ul[@data-interval="%s"]/li/a/div[@class="Tt2J2"]''' % date_today
    xPATH_link = '''//ul[@data-interval="%s"]/li/a/div[@class="Tt2J2"]/..''' % date_today
    xPATH_button = '''/div/div[2]/button'''
    # print(date_today)

    driver.get(URL)
    # time.sleep(3)
    # driver.find_element(By.XPATH, xPATH_button).click()
    # ищет новости на сегодня
    cell_news_arr = []
    cell_news = driver.find_elements(By.XPATH, xPATH)
    for i in cell_news:
        cell_news_arr.append(i.text)
    # print(cell_news_arr)
    # print(date_today)

    # поиск ссылок
    news_link_arr = []
    news_link = driver.find_elements(By.XPATH, xPATH_link)
    for j in news_link:
        a_link = j.get_attribute('href')
        news_link_arr.append(a_link)
    # print(news_link_arr)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">forbes.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.forbes.ru/ нет сегодня новостей!')
    print('forbes.ru', type(message_text))
    print(message_text)
    # return message_text
    driver.quit()
forbes_ru()

print("--- %s seconds ---" % (time.time() - start_time))