import datetime
import time
from babel.dates import format_date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import threading
from babel.dates import format_date, format_datetime
import pprint
import asyncio
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from lxml import etree
import re


# работа браузера без интерфейса
option = Options()
option.headless = True

# # proxy-server //japan
# chrome_options = webdriver.ChromeOptions()
# PROXY = "103.124.2.229:3128"
# chrome_options.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(options=option)
driver.set_window_size(1920, 1080)

x = datetime.datetime.today()
x2 = datetime.datetime.date(x)
date_today = format_date(x2, locale='de_DE')



AllParseResult = ""

def GetParseResult():

    return AllParseResult

async def MainParser():
    task1 = asyncio.create_task(zerno_ru())
    task2 = asyncio.create_task(zol_ru())
    task3 = asyncio.create_task(agroinvestor_ru())
    task4 = asyncio.create_task(agriculture_com())
    task5 = asyncio.create_task(forbes_ru())
    task6 = asyncio.create_task(spglobal_com())
    await asyncio.wait([task1, task2, task3, task4, task5, task6])
    # await asyncio.wait([task1])

    try:
        global AllParseResult
        AllParseResult = task1.result() + task2.result() + task3.result() + task4.result() + task5.result() + task6.result()
        # print('ПОЛНЫЙ СПИСОК', a)
    except Exception:
        print('ОШИБКА ПОИСКА')

    print('ЗАВЕРШЕНО')





# --------------------------- ПАРСЕРЫ ------------------------------

async def zerno_ru():

    # date_today = '03.12.2021'
    xPATH = '''//*[text()='%s']//../../span[2]/span/a''' % date_today
    xPATH_link = '''//*[text()='%s']//../../span[2]/span/a/@href''' % date_today

    URL = 'https://zerno.ru/news_list'
    # response = urlopen(url)
    # htmlparser = etree.HTMLParser()
    # tree = etree.parse(response, htmlparser)
    # a = tree.xpath(xPATH_link)
    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    count_index = dom.xpath(xPATH)
    # count_index = len(count_index)

    # поиск содержимого блоков
    cell_news_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH)[i].text
        cell_news_arr.append(a)
    # print(cell_news_arr)

    # поиск ссылок на содержимое блоков
    news_link_arr = []
    for i in range(0, len(count_index)):
            a = dom.xpath(xPATH_link)[i]
            news_link_arr.append(a)
    # print(news_link_arr)
    full_links = []
    for i in news_link_arr:
        first_part_link = 'https://zerno.ru'
        i = first_part_link + i
        full_links.append(i)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, full_links)]
    # print(message_text)


    return message_text


async def zol_ru():

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


    # поиск индекс строки с датой, проверка массива на пустоту
    # print(date_today)
    try:
        index_elem = pre_mass.index(date_today)
    except ValueError:
        print('На сайте https://www.zol.ru/ (2) нет сегодня новостей!')
        return
    del pre_mass[index_elem:]
    del pre_mass[0]
    # print(pre_mass)

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
    # print(message_text)

    # for x in message_text:
    #     bot.send_message(message.chat.id, x, disable_web_page_preview=True, parse_mode='html')

    return message_text



async def agroinvestor_ru():

    # BS4
    URL = 'https://www.agroinvestor.ru/'

    date_today = format_date(x2, "d MMMM yyyy", locale='ru')
    # date_today = '2 декабря 2021'

    xPATH = '''//*[text()='%s']/../../a/h3''' % date_today
    xPATH_link = '''//*[text()='%s']/../../a[2]/@href''' % date_today

    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    count_index = dom.xpath(xPATH)


    # поиск содержимого блоков
    cell_news_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH)[i].text
        cell_news_arr.append(a)
    # print(cell_news_arr)

    # поиск ссылок на содержимое блоков
    news_link_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH_link)[i]
        news_link_arr.append(a)
    # print(news_link_arr)


    first_part_link = 'https://www.agroinvestor.ru'
    link_news = []
    for i in news_link_arr:
        i = first_part_link + i
        link_news.append(i)
    # print(link_news)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in link_news:
        # link = re.sub(r'\b-', '\-', link)
        # print(link)
        link1 = '<a href="%s">agroinvestor.ru</a>' % link

        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]

    # for x in message_text:
    #     bot.send_message(message.chat.id, x, disable_web_page_preview=True, parse_mode='html')

    return message_text


async def agriculture_com():

    # BS4

    URL = 'https://www.agriculture.com/search?search_api_views_fulltext=&sort_by=created'

    # date_today = '12.07.2021'
    date_today = format_date(x2, "MM.dd.yyy", locale='ru')
    xPATH = '''//*[contains(text(),'%s')]/../h2/a''' % date_today
    xPATH_link = '''//*[contains(text(),'%s')]/../h2/a/@href''' % date_today

    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    count_index = dom.xpath(xPATH)
    # count_index = len(count_index)

    # поиск содержимого блоков НА 1 СТРАНИЦЕ
    cell_news_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH)[i].text
        cell_news_arr.append(a)
    # print(cell_news_arr)

    # поиск ссылок на содержимое блоков
    news_link_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH_link)[i]
        news_link_arr.append(a)

    # поиск содержимого блоков НА СЛЕДУЮЩИХ СТРАНИЦАХ
    def drug_data(page_number):
        URL = 'https://www.agriculture.com/search?search_api_views_fulltext=&sort_by=created&page=' + str(page_number)
        # print(URL)
        webpage = requests.get(URL)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup))
        count_index = dom.xpath(xPATH)

        for i in range(0, len(count_index)):
            a = dom.xpath(xPATH)[i].text
            cell_news_arr.append(a)

        for i in range(0, len(count_index)):
            a = dom.xpath(xPATH_link)[i]
            news_link_arr.append(a)

    for x in range(1, 3):
        drug_data(x)

    # print(cell_news_arr)
    # print(news_link_arr)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">agriculture.com</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    # print(message_text)

    # for x in message_text:
    #     bot.send_message(message.chat.id, x, disable_web_page_preview=True, parse_mode='html')

    return message_text

async def apk_inform_com():
    URL = 'https://www.apk-inform.com/ru/news/russia'

    xPATH = '''//*[contains(text(),'Сегодня')]/../../../../..//a[@class='text']'''
    xPATH_link = '''//*[contains(text(),'Сегодня')]/../../../../..//a[@class='text']/@href'''

    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    count_index = dom.xpath(xPATH)
    # count_index = len(count_index)

    # поиск содержимого блоков НА 1 СТРАНИЦЕ
    cell_news_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH)[i].text
        cell_news_arr.append(a)
    # print(cell_news_arr)

    # поиск ссылок на содержимое блоков
    news_link_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH_link)[i]
        first_part_link = 'https://www.apk-inform.com'
        a = first_part_link + a
        news_link_arr.append(a)
    # print(news_link_arr)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">apk-inform.com</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    return message_text



#--------------------------- SELENIUM ------------------------------------
async def forbes_ru():
    # date_today = '03.12.2021'


    URL = 'https://www.forbes.ru/'
    xPATH = '''//ul[@data-interval="%s"]/li/a/div[@class="Tt2J2"]''' % date_today
    xPATH_link = '''//ul[@data-interval="09.12.2021"]/li/a/div[@class="Tt2J2"]/..'''

    driver.get(URL)

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
    forbes_massive = message_text

    # driver.quit()

    return forbes_massive


async def spglobal_com():

    URL = '''https://www.spglobal.com/platts/en/search-results?q='''

    date_today = format_date(x2, "d MMM yyy", locale='en')
    # print(date_today)

    xPATH = '''//li[contains(.,"%s")]/div/a/h5''' % date_today
    xPATH_link = '''//li[contains(.,"%s")]/div/a''' % date_today

    driver.get(URL)
    # кнопка "Load more"

    # for i in range(3):
    #     try:
    #         loadMoreButton = driver.find_element(By.XPATH,
    #                                              '/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div[1]/a/span')
    #         time.sleep(3)
    #         loadMoreButton.click()
    #         time.sleep(3)
    #         print('receive button!')
    #     except Exception as e:
    #         print(e, '\n')
    #         break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    loadMoreButton = driver.find_element(By.XPATH, '//*[@id="loadSearch"]/a/span')
    time.sleep(3)
    loadMoreButton.click()
    time.sleep(5)
    print('receive button!')

    # ищет новости на сегодня
    cell_news_arr = []
    cell_news = driver.find_elements(By.XPATH, xPATH)
    for i in cell_news:
        cell_news_arr.append(i.text)
    # print(cell_news_arr)


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
        link1 = '<a href="%s">spglobal.com</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    # print(message_text)
    return message_text


async def rbc_ru():
    URL = '''https://www.rbc.ru/search/?query=+&project=rbcnews&dateFrom=%s&dateTo=%s''' % (date_today, date_today)
    # print(URL)
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    date_yesterday = format_date(yesterday, "dd MMM", locale='ru')
    date_yesterday = str(date_yesterday).replace('.', '')
    print(date_yesterday)


    # xPATH = '''//div[@class="search-item js-search-item"]/div/a/span/span[1]'''
    xPATH = '''//div[@class="js-news-feed-list"]/a/div/div/span[1]'''
    xPATH_link = '''//div[@class="js-news-feed-list"]/a/@href'''
    xPATH_yesterday = '''//span[contains(.,"%s")]/../span[@class="news-feed__item__title"]''' % date_yesterday

    driver.get(URL)
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

    b = [1]
    # отсечь лишние новости
    for i in range(1):
        a = dom.xpath(xPATH_yesterday)[i].text
        a = re.sub("^\s+|\n|\r|\xa0|\s+$", '', a)
        yesterday_new = a
        print(yesterday_new)
    # входит ли yesterday_new в список новостей?
    if yesterday_new in cell_news_arr:
        print(True)
    else:
        print(False)
    try:
        index_yesterday_new = cell_news_arr.index(yesterday_new)
    except Exception as e:
        print(e)
    cell_news_arr = cell_news_arr[:index_yesterday_new]

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
    # print(message_text)

    return message_text


async def ria_ru_1():
    URL = '''https://ria.ru/world/'''
    # --ЕСТЬ, НО НЕТ--
    # '''//div[contains(text(), ":")][not(contains(text(), ","))]'''
    xPATH = '''//div[contains(text(), ":")][not(contains(text(), ","))]/../../div/a[2]'''
    xPATH_link = '''//div[contains(text(), ":")][not(contains(text(), ","))]/../../div/a[2]'''
    xPATH_LoadMore = '''/html/body/div[10]/div[2]/div/div[4]/div/div[1]/div/div[3]'''
    xPATH_Period = '''//*[@class="pmu-saturday pmu-selected pmu-selected-first pmu-selected-last pmu-today pmu-button"]'''

    driver.get(URL)

    # # Выставление периода
    # time.sleep(2)
    # driver.find_element(By.XPATH, '//*[@class="list-date"]').click()
    # time.sleep(3)
    # driver.find_element(By.XPATH, xPATH_Period).click()
    # time.sleep(2)
    # driver.find_element(By.XPATH, xPATH_Period).click()
    # print('Период выставлен')
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    # Load more
    driver.find_element(By.XPATH, xPATH_LoadMore).click()
    # print('Load more')
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ищет новости на сегодня и ссылки
    cell_news_arr = []
    news_link_arr = []
    cell_news = driver.find_elements(By.XPATH, xPATH)
    for i in cell_news:
        cell_news_arr.append(i.text)
        a_link = i.get_attribute('href')
        news_link_arr.append(a_link)
    # print(cell_news_arr)
    # print(news_link_arr)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">ria.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    # print(message_text)

    return message_text


async def ria_ru_2():
    URL = '''https://ria.ru/politics/'''
    # --ЕСТЬ, НО НЕТ--
    # '''//div[contains(text(), ":")][not(contains(text(), ","))]'''
    xPATH = '''//div[contains(text(), ":")][not(contains(text(), ","))]/../../div/a[2]'''
    xPATH_link = '''//div[contains(text(), ":")][not(contains(text(), ","))]/../../div/a[2]'''
    xPATH_LoadMore = '''/html/body/div[10]/div[2]/div/div[4]/div/div[1]/div/div[3]'''
    xPATH_Period = '''//*[@class="pmu-saturday pmu-selected pmu-selected-first pmu-selected-last pmu-today pmu-button"]'''

    driver.get(URL)

    # # Выставление периода
    # time.sleep(2)
    # driver.find_element(By.XPATH, '//*[@class="list-date"]').click()
    # time.sleep(3)
    # driver.find_element(By.XPATH, xPATH_Period).click()
    # time.sleep(2)
    # driver.find_element(By.XPATH, xPATH_Period).click()
    # print('Период выставлен')

    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(3)
    # # Load more
    # driver.find_element(By.XPATH, xPATH_LoadMore).click()
    # # print('Load more')
    # time.sleep(3)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # ищет новости на сегодня и ссылки
    cell_news_arr = []
    news_link_arr = []
    cell_news = driver.find_elements(By.XPATH, xPATH)
    for i in cell_news:
        cell_news_arr.append(i.text)
        a_link = i.get_attribute('href')
        news_link_arr.append(a_link)
    # print(cell_news_arr)
    # print(news_link_arr)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">ria.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    # print(message_text)

    return message_text

def ria_ru_3():
    URL = '''https://ria.ru/economy/'''
    # --ЕСТЬ, НО НЕТ--
    # '''//div[contains(text(), ":")][not(contains(text(), ","))]'''
    xPATH = '''//div[contains(text(), ":")][not(contains(text(), ","))]/../../div/a[2]'''
    xPATH_link = '''//div[contains(text(), ":")][not(contains(text(), ","))]/../../div/a[2]'''
    xPATH_LoadMore = '''/html/body/div[10]/div[2]/div/div[4]/div/div[1]/div/div[3]'''
    xPATH_Period = '''//*[@class="pmu-saturday pmu-selected pmu-selected-first pmu-selected-last pmu-today pmu-button"]'''

    driver.get(URL)

    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    try:
        # Load more
        driver.find_element(By.XPATH, xPATH_LoadMore).click()
        # print('Load more')
    except Exception as e:
        print(e)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # ищет новости на сегодня и ссылки
    cell_news_arr = []
    news_link_arr = []
    cell_news = driver.find_elements(By.XPATH, xPATH)
    for i in cell_news:
        cell_news_arr.append(i.text)
        a_link = i.get_attribute('href')
        news_link_arr.append(a_link)
    # print(cell_news_arr)
    # print(news_link_arr)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">ria.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    # print(message_text)

    return message_text


def tass_ru_1():
    URL_LINKS = ['''https://tass.ru/msp''', '''https://tass.ru/ekonomika''', '''https://tass.ru/politika''']
    # --ЕСТЬ, НО НЕТ--
    # '''//div[contains(text(), ":")][not(contains(text(), ","))]'''
    xPATH = '''//span[contains(text(), "сегодня,")or(contains(text(), "назад"))]/../../div[2]/div[3]/div/span[1]'''
    xPATH_link = '''//span[contains(text(), "сегодня,")or(contains(text(), "назад"))]/../../../../../a'''

    all_info = []
    for URL in URL_LINKS:
        driver.get(URL)
        time.sleep(3)

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        except Exception as e:
            print(e)

        # ищет новости на сегодня и ссылки
        cell_news_arr = []
        cell_news = driver.find_elements(By.XPATH, xPATH)
        for i in cell_news:
            cell_news_arr.append(i.text)
        cell_news_arr = [x for x in cell_news_arr if x]
        # print(cell_news_arr)

        news_link_arr = []
        link_news = driver.find_elements(By.XPATH, xPATH_link)
        for i in link_news:
            a_link = i.get_attribute('href')
            news_link_arr.append(a_link)
        # print(news_link_arr)

        # преобразование ссылок в нужный вид
        link_mass = []
        for link in news_link_arr:
            link1 = '<a href="%s">tass.ru</a>' % link
            link_mass.append(link1)

        message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
        for x in message_text:
            all_info.append(x)
    # print(all_info)

    return all_info

def tass_ru_2():
    URL = '''https://tass.ru/obschestvo'''
    # --ЕСТЬ, НО НЕТ--
    # '''//div[contains(text(), ":")][not(contains(text(), ","))]'''
    # проверка содержания ссылок  -- //*[contains(@href ,'nomika/13175455')]
    xPATH = '''//span[contains(text(), "сегодня,")or(contains(text(), "назад"))]/../../div[2]/div[3]/div/span[1]'''
    xPATH_link = '''//span[contains(text(), "сегодня,")or(contains(text(), "назад"))]/../../../../../a'''

    driver.get(URL)

    time.sleep(3)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    except Exception as e:
        print(e)

    # ищет новости на сегодня и ссылки
    cell_news_arr = []
    cell_news = driver.find_elements(By.XPATH, xPATH)
    for i in cell_news:
        cell_news_arr.append(i.text)
    cell_news_arr = [x for x in cell_news_arr if x]
    # print(cell_news_arr)
    # print(len(cell_news_arr))

    news_link_arr = []
    link_news = driver.find_elements(By.XPATH, xPATH_link)
    for i in link_news:
        a_link = i.get_attribute('href')
        news_link_arr.append(a_link)
    # pprint.pprint(news_link_arr)
    # print(news_link_arr)
    # print(len(news_link_arr))

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in news_link_arr:
        link1 = '<a href="%s">tass.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    # pprint.pprint(message_text)

    return message_text






# --------------------- ПОТОКИ/ТАЙМЕР -----------------------------
def executeSomething():
    print(AllParseResult)
    asyncio.run(MainParser())
    t = threading.Timer(60.0, executeSomething)  #600.0
    t.start()

executeSomething()

    # aboba = True
# while aboba == True: