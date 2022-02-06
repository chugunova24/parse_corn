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

def lenta_ru_politic():
    # --ЕСТЬ, НО НЕТ--
    # '''//div[contains(text(), ":")][not(contains(text(), ","))]'''

    # mounth_today = date_today = format_date(x2, "MMMM", locale='ru_RU')
    year = str(format_date(x2, "YYY", locale='ru_RU'))
    year_last = str(int(year) - 1)

    URL = ['''https://lenta.ru/rubrics/world/politic/1/''', '''https://lenta.ru/rubrics/world/politic/2/''',
           '''https://lenta.ru/rubrics/world/politic/3/''', '''https://lenta.ru/rubrics/world/politic/4/''',
           '''https://lenta.ru/rubrics/world/politic/5/''', '''https://lenta.ru/rubrics/world/politic/6/''',
           '''https://lenta.ru/rubrics/world/politic/7/''', '''https://lenta.ru/rubrics/world/politic/8/''']

    news_link_arr = []
    cell_news_arr = []
    for i in URL:
        # print(i)
        xPATH = '''//time[contains(text(), ":")][not(contains(text(), "%s"))][not(contains(text(), "%s"))]/../../h3''' % (year, year_last)
        xPATH_link = '''//time[contains(text(), ":")][not(contains(text(), "%s"))][not(contains(text(), "%s"))]/../../@href''' % (year, year_last)

        webpage = requests.get(i)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup))
        count_index = dom.xpath(xPATH)

        for i in range(0, len(count_index)):
            a = dom.xpath(xPATH)[i].text
            cell_news_arr.append(a)

        for i in range(0, len(count_index)):
            a = dom.xpath(xPATH_link)[i]
            news_link_arr.append(a)
    # print(cell_news_arr)
    # print(news_link_arr)

    # преобразование ссылок
    first_part_link = 'https://lenta.ru'
    link_news = []
    for i in news_link_arr:
        i = first_part_link + i
        link_news.append(i)
    # print(link_news)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in link_news:
        link = re.sub("^\s+|\n|\r|\xa0|\s+$", '', link)
        link1 = '<a href="%s">lenta.ru</a>' % link

        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://lenta.ru/rubrics/world/politic/1/ нет сегодня новостей!')
    # print(message_text)
    print('lenta.ru/rubrics/world/politic', type(message_text))
    return message_text

lenta_ru_politic()

print("--- %s seconds ---" % (time.time() - start_time))