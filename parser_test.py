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

def rbc_ru():
    URL = '''https://www.rbc.ru/search/?query=+&project=rbcnews&dateFrom=%s&dateTo=%s''' % (date_today, date_today)

    yesterday = x.replace(day=1) - datetime.timedelta(days=1)
    mounth = str(format_date(x2, "MMMM", locale='ru')[:3])
    mounth_last = str(format_date(yesterday, "MMMM", locale='ru')[:3])


    xPATH = '''//*[@class='news-feed__item__date-text'][not(contains(text(), "%s"))][not(contains(text(), "%s"))]//../../span[contains(@class, 'news-feed__item__title')]''' % (mounth, mounth_last)
    xPATH_link = '''//*[@class='news-feed__item__date-text'][not(contains(text(), "%s"))][not(contains(text(), "%s"))]//../../span[contains(@class, 'news-feed__item__title')]//..//../../@href''' % (mounth, mounth_last)

    driver.get(URL)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as e:
        print('rbc_ru:', e)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    dom = etree.HTML(str(soup))
    count_index = dom.xpath(xPATH)

    # поиск содержимого блоков
    cell_news_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH)[i].text
        a = re.sub("^\s+|\n|\r|\xa0|\s+$", '', a)
        cell_news_arr.append(a)
    # print(cell_news_arr)

    # поиск ссылок на содержимое блоков
    news_link_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH_link)[i]
        news_link_arr.append(a)
    # print(news_link_arr)

    len_cell_mass = len(cell_news_arr)
    news_link_arr = news_link_arr[:len_cell_mass]

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">rbc.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.rbc.ru/search нет сегодня новостей!')
    # print(message_text)
    print('rbc.ru', type(message_text))

    return message_text

rbc_ru()

print("--- %s seconds ---" % (time.time() - start_time))