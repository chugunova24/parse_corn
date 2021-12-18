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

# chrome_options = webdriver.ChromeOptions()
PROXY = "103.124.2.229:3128"
option.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(options=option)
driver.set_window_size(1920, 1080)

x = datetime.datetime.today()
x2 = datetime.datetime.date(x)
date_today = format_date(x2, locale='de_DE')

def reuters_com():
    URL = '''https://www.reuters.com/markets/commodities/'''

    xPATH1 = '''//time[contains(text(), "MSK")]/../../div[2]/a'''
    xPATH_link1 = '''//time[contains(text(), "MSK")]/../../div[2]/a'''

    xPATH2 = '''//time[contains(text(), "MSK")]/../span[2]'''
    xPATH_link2 = '''//time[contains(text(), "MSK")]/../../a'''
    xPATH_button = '''//div[@class="Topic__loadmore___3juLCQ"]/button/div/span'''

    driver.get(URL)
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.find_element(By.XPATH, xPATH_button).click()
    except Exception as e:
        print(e)
    # agent = driver.execute_script("return navigator.userAgent")
    # print(agent)

    # ищет новости на сегодня
    cell_news_arr = []
    cell_news = driver.find_elements(By.XPATH, xPATH1)
    for i in cell_news:
        cell_news_arr.append(i.text)
    # print(cell_news_arr)

    cell_news = driver.find_elements(By.XPATH, xPATH2)
    for i in cell_news:
        cell_news_arr.append(i.text)
    # print(cell_news_arr)
    print(len(cell_news_arr))

    # ссылки
    news_link_arr = []
    link_news = driver.find_elements(By.XPATH, xPATH_link1)
    for i in link_news:
        a_link = i.get_attribute('href')
        news_link_arr.append(a_link)
    # pprint(news_link_arr)
    # print()

    link_news = driver.find_elements(By.XPATH, xPATH_link2)
    for i in link_news:
        a_link = i.get_attribute('href')
        news_link_arr.append(a_link)
    # pprint.pprint(news_link_arr)
    print(len(news_link_arr))

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">reuters.com</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    pprint(message_text)


    driver.quit()
    # return message_text



reuters_com()




print("--- %s seconds ---" % (time.time() - start_time))