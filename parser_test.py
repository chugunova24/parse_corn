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

def zol_ru():

    # BS4
    if datetime.date.today().weekday() == 0:
        yesterday = datetime.datetime.now() - datetime.timedelta(2)
    else:
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
    date_today = format_date(yesterday, "d MMMM yyy", locale='ru')
    # date_today = '2 декабря 2021'

    URL = 'https://www.zol.ru/news/grain/'
    xPATH = '''//tr'''
    xPATH_link = '''//a[@class='news_block']'''


    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.text, 'lxml')
    quotes = soup.findAll('td')
    # print(quotes)

    mass = []
    for quote in quotes:
        # print(quote.text)
        mass.append(quote.text)
    # print(mass)

    pre_mass = []
    for i in mass:
        i = re.sub("^\s+|\n|\r|\s+$", '', i)
        pre_mass.append(i)
    # print(pre_mass)


    # поиск индекса строки с датой, проверка массива на пустоту
    # print(date_today)
    try:
        index_elem = pre_mass.index(date_today)
        del pre_mass[index_elem:]
        del pre_mass[0]
        # print(pre_mass)
    except Exception as e:
        print('На сайте https://www.zol.ru/ (2) нет сегодня новостей!')
        return

    for i in pre_mass:
        if len(i) == 5:
            pre_mass.remove(i)
    # print(pre_mass)

    # # поиск ссылок на содержимое блоков
    link_mass = soup.findAll('a', class_='news_block')
    # print(link_mass)

    l_mass = []
    for i in link_mass:
        i = i.get('href')
        l_mass.append(i)

    # подсчитаем кол-во новостей за сегодня и сравняем кол-во ссылок
    len_pre_mass = len(pre_mass)
    # print(len_pre_mass)
    len_l_mass = len(l_mass)
    # print(len_l_mass)
    link = l_mass[:len_pre_mass]
    # print(len(link))

    part_link_part = '''https://www.zol.ru'''
    link_news = []
    for i in link:
        i = part_link_part + i
        link_news.append(i)
    # print(link_news)

    link_mass = []
    for link in link_news:
        # link = re.sub(r'\b-', '\-', link)
        # print(link)
        link1 = '<a href="%s">zol.ru</a>' % link
        # print(link1)
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(pre_mass, link_mass)]
    print(message_text)

    # for x in message_text:
    #     bot.send_message(message.chat.id, x, disable_web_page_preview=True, parse_mode='html')
    print('zol.ru', type(message_text))

    if message_text != []:
        return message_text

zol_ru()



print("--- %s seconds ---" % (time.time() - start_time))