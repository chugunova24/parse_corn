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
import itertools
import os


# работа браузера без интерфейса
option = Options()
# option = webdriver.ChromeOptions()
# option.headless = True

option.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
# option.binary_location = GOOGLE_CHROME_BIN
# option.binary_location = os.environ.get('GOOGLE_CHROME_SHIM', None)
# executable_path=os.environ.get('CHROMEDRIVER_PATH'),
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-gpu')
option.add_argument('--disable-dev-shm-usage')

# # proxy-server //japan
# chrome_options = webdriver.ChromeOptions()
# PROXY = "103.124.2.229:3128"
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
# PROXY = "103.124.2.229:3128"
# option.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), options=option)
# driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=option)
driver.set_window_size(1920, 1080)

x = datetime.datetime.today()
x2 = datetime.datetime.date(x)
date_today = format_date(x2, locale='de_DE')



AllParseResult = []

def GetParseResult():
    return AllParseResult

async def MainParser():
    task1 = asyncio.create_task(zerno_ru())
    task2 = asyncio.create_task(zol_ru())
    task3 = asyncio.create_task(agroinvestor_ru())
    task4 = asyncio.create_task(agriculture_com())
    task5 = asyncio.create_task(apk_inform_com())
    task6 = asyncio.create_task(oilworld_ru())
    task7 = asyncio.create_task(interfax_ru())
    task8 = asyncio.create_task(lenta_ru_politic())
    task9 = asyncio.create_task(lenta_ru_economics())
    task10 = asyncio.create_task(forbes_ru())
    task11 = asyncio.create_task(spglobal_com())
    task12 = asyncio.create_task(rbc_ru())
    task13 = asyncio.create_task(ria_ru_1())
    task14 = asyncio.create_task(ria_ru_2())
    task15 = asyncio.create_task(ria_ru_3())
    task16 = asyncio.create_task(tass_ru_1())
    task17 = asyncio.create_task(tass_ru_2())
    task18 = asyncio.create_task(kommersant_ru_economics())
    task19 = asyncio.create_task(kommersant_ru_politics())
    task20 = asyncio.create_task(kommersant_ru_business())
    task21 = asyncio.create_task(kommersant_ru_consumer_market())
    task22 = asyncio.create_task(kommersant_ru_finances())

    await asyncio.wait([task1, task2, task3, task4, task5, task6, task7, task8, task9, task10, task11, task12, task13, \
                        task14, task15, task16, task17, task18, task19, task20, task21, task22])
    # await asyncio.wait([task1, task2])

    try:
        global AllParseResult
        # AllParseResult = list(itertools.chain(task1.result(), task2.result()))
                         # task1.result() + task2.result()
                         # + task3.result() + task4.result()
                         # + task5.result() + \
                         # task6.result() + task7.result() + task8.result() + task9.result() + task10.result() + \
                         # task11.result() + task12.result() + task13.result() + task14.result() + task15.result() + \
                         # task16.result() + task17.result() + task18.result() + task19.result() + task20.result() + \
                         # task21.result() + task22.result()

        # С проверкой на None!
        AllTasks = [task1.result(), task2.result(), task3.result(), task4.result(), task5.result(),\
                    task6.result(), task7.result(), task8.result(), task9.result(), task10.result(), \
                    task11.result(), task12.result(), task13.result(), task14.result(), task15.result(), \
                    task16.result(), task17.result(), task18.result(), task19.result(), task20.result(), \
                    task21.result(), task22.result()]
        print('ОБЩИЙ ЛИСТ СОЗДАН')
        for i in AllTasks:
            if i != None:
                AllParseResult.extend(i)
        print('ПОЛНЫЙ СПИСОК', AllParseResult)
    except Exception as e:
        print('ОШИБКА ПОИСКА', e)
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

    link_mass = []
    for link in full_links:
        # link = re.sub(r'\b-', '\-', link)
        # print(link)
        link1 = '<a href="%s">zol.ru</a>' % link
        # print(link1)
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    # print(message_text)
    print('zerno.ru', type(message_text))

    if message_text != []:
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


    # поиск индекса строки с датой, проверка массива на пустоту
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
    print('zol.ru', type(message_text))

    if message_text != []:
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
    if message_text == []:
        print('На сайте https://www.agroinvestor.ru/ нет сегодня новостей!')

    # for x in message_text:
    #     bot.send_message(message.chat.id, x, disable_web_page_preview=True, parse_mode='html')
    print('agroinvestor.ru', type(message_text))

    if message_text != []:
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
    if message_text == []:
        print('На сайте https://www.agriculture.com/search?search_api_views_fulltext=&sort_by=created нет сегодня новостей!')
    # print(message_text)

    # for x in message_text:
    #     bot.send_message(message.chat.id, x, disable_web_page_preview=True, parse_mode='html')
    print('agriculture.com', type(message_text))

    if message_text != []:
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
    if message_text == []:
        print('На сайте https://www.apk-inform.com/ru/news/russia нет сегодня новостей!')
    print('apk-inform.com', type(message_text))
    return message_text


async def oilworld_ru():
    URL = '''https://www.oilworld.ru/news/all'''

    # date_today = '12.07.2021'
    date_today = format_date(x2, "yyy", locale='ru')
    # print(date_today)
    next_year = int(date_today) - 1
    # print(next_year)
    # //div[contains(text(), ":")][not(contains(text(), "2021"))]
    # //span[contains(text(), ":")][not(contains(text(), "2021"))][not(contains(text(), "2022"))]/../a

    xPATH = '''//span[contains(text(), ":")][not(contains(text(), "%s"))][not(contains(text(), "%s"))]/../a/@title''' \
            % (date_today, str(next_year))
    xPATH_link = '''//span[contains(text(), ":")][not(contains(text(), "%s"))][not(contains(text(), "%s"))]/../a/@href''' \
                 % (date_today, str(next_year))

    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    count_index = dom.xpath(xPATH)
    # print(soup)

    # поиск содержимого блоков НА 1 СТРАНИЦЕ
    cell_news_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH)[i]
        cell_news_arr.append(a)
    # print(cell_news_arr)

    # поиск ссылок на содержимое блоков НА 1 СТРАНИЦЕ
    news_link_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH_link)[i]
        news_link_arr.append(a)

    # print(news_link_arr)

    def search_through_pages():
        for i in range(2, 4):
            URL = '''https://www.oilworld.ru/news/all?page=%s''' % str(i)
            # print(URL)

            webpage = requests.get(URL)
            soup = BeautifulSoup(webpage.content, "html.parser")
            dom = etree.HTML(str(soup))
            count_index = dom.xpath(xPATH)

            for i in range(0, len(count_index)):
                a = dom.xpath(xPATH)[i]
                cell_news_arr.append(a)

            for i in range(0, len(count_index)):
                a = dom.xpath(xPATH_link)[i]
                news_link_arr.append(a)
    search_through_pages()
    # print(cell_news_arr)
    # print(news_link_arr)

    # преобразование ссылок
    first_part_link = 'https://www.oilworld.ru'
    link_news = []
    for i in news_link_arr:
        i = first_part_link + i
        link_news.append(i)
    # print(link_news)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in link_news:
        link = re.sub("^\s+|\n|\r|\xa0|\s+$", '', link)
        link1 = '<a href="%s">oilworld.ru</a>' % link

        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.oilworld.ru/news/all нет сегодня новостей!')
    # print(message_text)
    print('oilworld.ru', type(message_text))
    return message_text



async def interfax_ru():

    year_today = format_date(x2, "yyy", locale='ru')
    mounth_today = format_date(x2, "MM", locale='ru')
    day_today = format_date(x2, "dd", locale='ru')
    URL = '''https://www.interfax.ru/news/%s/%s/%s''' % (year_today,mounth_today,day_today)
    # print(URL)

    # //div[contains(text(), ":")][not(contains(text(), "2021"))]
    # //span[contains(text(), ":")][not(contains(text(), "2021"))][not(contains(text(), "2022"))]/../a

    xPATH = '''//div[@data-id]/a/h3'''
    xPATH_link = '''//div[@data-id]/a/@href'''

    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    count_index = dom.xpath(xPATH)
    # print(soup)

    # поиск содержимого блоков НА 1 СТРАНИЦЕ
    cell_news_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH)[i].text
        cell_news_arr.append(a)
    # print(cell_news_arr)

    # поиск ссылок на содержимое блоков НА 1 СТРАНИЦЕ
    news_link_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH_link)[i]
        news_link_arr.append(a)
    # print(news_link_arr)

    def search_through_pages():
        for i in range(2, 6):
            URL = '''https://www.interfax.ru/news/%s/%s/%s/all/page_%s''' % (year_today,mounth_today,day_today, str(i))
            print(URL)

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
    search_through_pages()
    # print(cell_news_arr)
    # print(news_link_arr)

    # преобразование ссылок
    first_part_link = 'https://www.interfax.ru'
    link_news = []
    for i in news_link_arr:
        if i[0] == "/":
            i = first_part_link + i
            link_news.append(i)
        else:
            link_news.append(i)
    # print(link_news)

    # преобразование ссылок в нужный вид
    link_mass = []
    for link in link_news:
        link = re.sub("^\s+|\n|\r|\xa0|\s+$", '', link)
        link1 = '<a href="%s">interfax.ru</a>' % link

        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.interfax.ru/news нет сегодня новостей!')
    # print(message_text)
    print('interfax.ru', type(message_text))
    return message_text

async def lenta_ru_politic():
    # --ЕСТЬ, НО НЕТ--
    # '''//div[contains(text(), ":")][not(contains(text(), ","))]'''

    mounth_today = date_today = format_date(x2, "MMMM", locale='ru_RU')
    # print(mounth_today)
    URL = ['''https://lenta.ru/rubrics/world/politic/1/''', '''https://lenta.ru/rubrics/world/politic/2/''',
           '''https://lenta.ru/rubrics/world/politic/3/''', '''https://lenta.ru/rubrics/world/politic/4/''',
           '''https://lenta.ru/rubrics/world/politic/5/''', '''https://lenta.ru/rubrics/world/politic/6/''',
           '''https://lenta.ru/rubrics/world/politic/7/''', '''https://lenta.ru/rubrics/world/politic/8/''']

    news_link_arr = []
    cell_news_arr = []
    for i in URL:
        # print(i)
        xPATH = '''//time[contains(text(), ":")][not(contains(text(), "%s"))]/../../h3''' % mounth_today
        xPATH_link = '''//time[contains(text(), ":")][not(contains(text(), "%s"))]/../../@href''' % mounth_today

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


async def lenta_ru_economics():
    # --ЕСТЬ, НО НЕТ--
    # '''//div[contains(text(), ":")][not(contains(text(), ","))]'''

    mounth_today = date_today = format_date(x2, "MMMM", locale='ru_RU')
    # print(mounth_today)

    URL = '''https://lenta.ru/rubrics/economics/'''

    news_link_arr = []
    cell_news_arr = []

    # print(i)
    xPATH = '''//time[contains(text(), ":")][not(contains(text(), "%s"))]/../../../a/div/span''' % mounth_today
    xPATH_link = '''//time[contains(text(), ":")][not(contains(text(), "%s"))]/../../../a/@href''' % mounth_today

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
    # print(cell_news_arr)
    # print(news_link_arr)

    # преобразование ссылок
    first_part_link = 'https://lenta.ru'
    link_news = []
    for i in news_link_arr:
        if i[0] == "/":
            i = first_part_link + i
            link_news.append(i)
        else:
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
        print('На сайте https://lenta.ru/rubrics/economics/ нет сегодня новостей!')
    # print(message_text)
    print('lenta.ru/rubrics/economics/', type(message_text))
    return message_text







#--------------------------- SELENIUM ------------------------------------
async def forbes_ru():
    # date_today = '03.12.2021'

    URL = 'https://www.forbes.ru/'
    xPATH = '''//ul[@data-interval="%s"]/li/a/div[@class="Tt2J2"]''' % date_today
    xPATH_link = '''//ul[@data-interval="%s"]/li/a/div[@class="Tt2J2"]/..''' % date_today
    xPATH_button = '''/div/div[2]/button'''
    # print(date_today)

    try:
        driver.get(URL)
    except Exception as e:
        print('forbes_ru:', e)
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
    return message_text


async def spglobal_com():
    URL = '''https://www.spglobal.com/platts/en/search-results?q='''

    date_today = format_date(x2, "dd MMM yyy", locale='en')
    # print(date_today)

    xPATH = '''//li[contains(.,"%s")]/div/a/h5''' % date_today
    xPATH_link = '''//li[contains(.,"%s")]/div/a[1]''' % date_today

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

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        loadMoreButton = driver.find_element(By.XPATH, '//*[@id="loadSearch"]/a/span')
        time.sleep(3)
        loadMoreButton.click()
        time.sleep(5)
    except Exception as e:
        print('spglobal_com:', e)
    # print('receive button!')

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
    if message_text == []:
        print('На сайте https://www.spglobal.com/platts/en/search-results?q= нет сегодня новостей!')
    # pprint(message_text)
    print('spglobal.com', type(message_text))
    return message_text


async def rbc_ru():
    URL = '''https://www.rbc.ru/search/?query=+&project=rbcnews&dateFrom=%s&dateTo=%s''' % (date_today, date_today)
    # print(URL)
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    date_yesterday = format_date(yesterday, "dd MMM", locale='ru')
    date_yesterday = str(date_yesterday).replace('.', '')
    # print(date_yesterday)


    # xPATH = '''//div[@class="search-item js-search-item"]/div/a/span/span[1]'''
    xPATH = '''//div[@class="js-news-feed-list"]/a/div/div/span[1]'''
    xPATH_link = '''//div[@class="js-news-feed-list"]/a/@href'''
    xPATH_yesterday = '''//span[contains(.,"%s")]/../span[@class="news-feed__item__title"]''' % date_yesterday

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

    b = [1]
    # отсечь лишние новости
    for i in range(1):
        a = dom.xpath(xPATH_yesterday)[i].text
        a = re.sub("^\s+|\n|\r|\xa0|\s+$", '', a)
        yesterday_new = a
        # print(yesterday_new)
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
    if message_text == []:
        print('На сайте https://www.rbc.ru/search нет сегодня новостей!')
    # print(message_text)
    print('rbc.ru', type(message_text))

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
    try:
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
    except Exception as e:
        print('ria_ru_1:', e)

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
    if message_text == []:
        print('На сайте https://ria.ru/world/ нет сегодня новостей!')
    # print(message_text)
    print('ria.ru/world/', type(message_text))

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
    try:
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
    except Exception as e:
        print('ria_ru_2:', e)

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
    if message_text == []:
        print('На сайте https://ria.ru/politics/ нет сегодня новостей!')
    # print(message_text)
    print('ria.ru/politics/', type(message_text))

    return message_text

async def ria_ru_3():
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
        print('ria_ru_3:', e)
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
    if message_text == []:
        print('На сайте https://ria.ru/economy/ нет сегодня новостей!')
    # print(message_text)
    print('ria.ru/economy/', type(message_text))
    return message_text


async def tass_ru_1():
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
            print('tass_ru_1:', e)

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
    if all_info == []:
        print('На сайтах https://tass.ru/msp, https://tass.ru/ekonomika, https://tass.ru/politika нет сегодня новостей!')
    # print(all_info)
    print('https://tass.ru/msp, https://tass.ru/ekonomika, https://tass.ru/politika', type(all_info))
    return all_info

async def tass_ru_2():
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
        print('tass_ru_2:', e)

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
    if message_text == []:
        print('На сайте https://tass.ru/obschestvo нет сегодня новостей!')
    # pprint.pprint(message_text)
    print('tass.ru/obschestvo', type(message_text))

    return message_text





                 # ПАРСЕР С ПРОКСИ
# async def reuters_com():
#     URL = '''https://www.reuters.com/markets/commodities/'''
#
#     xPATH1 = '''//time[contains(text(), "MSK")]/../../div[2]/a'''
#     xPATH_link1 = '''//time[contains(text(), "MSK")]/../../div[2]/a'''
#
#     xPATH2 = '''//time[contains(text(), "MSK")]/../span[2]'''
#     xPATH_link2 = '''//time[contains(text(), "MSK")]/../../a'''
#     xPATH_button = '''//div[@class="Topic__loadmore___3juLCQ"]/button/div/span'''
#
#     driver.get(URL)
#     try:
#         time.sleep(2)
#         driver.find_element(By.XPATH, xPATH_button).click()
#         time.sleep(2)
#         driver.find_element(By.XPATH, xPATH_button).click()
#         time.sleep(1)
#         driver.find_element(By.XPATH, xPATH_button).click()
#         time.sleep(2)
#         driver.find_element(By.XPATH, xPATH_button).click()
#     except Exception as e:
#         print(e)
#     # agent = driver.execute_script("return navigator.userAgent")
#     # print(agent)
#
#     # ищет новости на сегодня
#     cell_news_arr = []
#     cell_news = driver.find_elements(By.XPATH, xPATH1)
#     for i in cell_news:
#         cell_news_arr.append(i.text)
#     # print(cell_news_arr)
#
#     cell_news = driver.find_elements(By.XPATH, xPATH2)
#     for i in cell_news:
#         cell_news_arr.append(i.text)
#     # print(cell_news_arr)
#     # print(len(cell_news_arr))
#
#     # ссылки
#     news_link_arr = []
#     link_news = driver.find_elements(By.XPATH, xPATH_link1)
#     for i in link_news:
#         a_link = i.get_attribute('href')
#         news_link_arr.append(a_link)
#     # pprint(news_link_arr)
#     # print()
#
#     link_news = driver.find_elements(By.XPATH, xPATH_link2)
#     for i in link_news:
#         a_link = i.get_attribute('href')
#         news_link_arr.append(a_link)
#     # pprint.pprint(news_link_arr)
#     # print(len(news_link_arr))
#
#     # преобразование ссылок в нужный вид
#     link_mass = []
#     for link in news_link_arr:
#         link1 = '<a href="%s">reuters.com</a>' % link
#         link_mass.append(link1)
#
#     message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
#     # print(message_text)
#
#     return message_text






async def kommersant_ru_economics():
    year_today = format_date(x2, "yyy", locale='ru')
    mounth_today = format_date(x2, "MM", locale='ru')
    day_today = format_date(x2, "dd", locale='ru')
    # print(year_today,mounth_today,day_today)
                # ДАТА!!!
    URL = 'https://www.kommersant.ru/archive/rubric/3/day/%s-%s-%s' % (year_today, mounth_today, day_today)
    # URL = '''https://www.kommersant.ru/archive/rubric/3/day/2018-06-14?page=2'''  # тест для кнопки "Показать ещё"
    # print(URL)
    xPATH = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_link = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_button = '''//*[contains(text(), "Показать еще")]'''

    driver.get(URL)

    # Кнопка "Показать ещё"
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
    except Exception as e:
        print('kommersant_ru_economics:', e)

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
        link1 = '<a href="%s">kommersant.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.kommersant.ru/archive/rubric/3/day нет сегодня новостей!')
    # print(message_text)
    print('kommersant.ru/archive/rubric/3', type(message_text))
    return message_text


async def kommersant_ru_politics():
    year_today = format_date(x2, "yyy", locale='ru')
    mounth_today = format_date(x2, "MM", locale='ru')
    day_today = format_date(x2, "dd", locale='ru')
    # print(year_today,mounth_today,day_today)
                # ДАТА!!!
    URL = 'https://www.kommersant.ru/archive/rubric/2/day/%s-%s-%s' % (year_today, mounth_today, day_today)
    # URL = '''https://www.kommersant.ru/archive/rubric/3/day/2018-06-14?page=2'''  # тест для кнопки "Показать ещё"
    # print(URL)
    xPATH = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_link = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_button = '''//*[contains(text(), "Показать еще")]'''

    driver.get(URL)

    # Кнопка "Показать ещё"
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
    except Exception as e:
        print('kommersant_ru_politics:', e)


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
        link1 = '<a href="%s">kommersant.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.kommersant.ru/archive/rubric/2/day нет сегодня новостей!')
    # print(message_text)
    print('kommersant.ru/archive/rubric/2', type(message_text))
    return message_text

async def kommersant_ru_business():
    year_today = format_date(x2, "yyy", locale='ru')
    mounth_today = format_date(x2, "MM", locale='ru')
    day_today = format_date(x2, "dd", locale='ru')
    # print(year_today,mounth_today,day_today)
                # ДАТА!!!
    URL = 'https://www.kommersant.ru/archive/rubric/4/day/%s-%s-%s' % (year_today, mounth_today, day_today)
    # URL = '''https://www.kommersant.ru/archive/rubric/3/day/2018-06-14?page=2'''  # тест для кнопки "Показать ещё"
    # print(URL)
    xPATH = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_link = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_button = '''//*[contains(text(), "Показать еще")]'''

    driver.get(URL)

    # Кнопка "Показать ещё"
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
    except Exception as e:
        print('kommersant_ru_business:', e)

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
        link1 = '<a href="%s">kommersant.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.kommersant.ru/archive/rubric/4/day нет сегодня новостей!')
    # print(message_text)
    print('kommersant.ru/archive/rubric/4', type(message_text))
    return message_text

async def kommersant_ru_consumer_market():
    year_today = format_date(x2, "yyy", locale='ru')
    mounth_today = format_date(x2, "MM", locale='ru')
    day_today = format_date(x2, "dd", locale='ru')
    # print(year_today,mounth_today,day_today)
                # ДАТА!!!
    URL = 'https://www.kommersant.ru/archive/rubric/41/day/%s-%s-%s' % (year_today, mounth_today, day_today)
    # URL = '''https://www.kommersant.ru/archive/rubric/3/day/2018-06-14?page=2'''  # тест для кнопки "Показать ещё"
    # print(URL)
    xPATH = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_link = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_button = '''//*[contains(text(), "Показать еще")]'''

    driver.get(URL)

    # Кнопка "Показать ещё"
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
    except Exception as e:
        print('kommersant_ru_consumer_market:', e)

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
        link1 = '<a href="%s">kommersant.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.kommersant.ru/archive/rubric/41/day нет сегодня новостей!')
    # print(message_text)
    print('kommersant.ru/archive/rubric/41', type(message_text))
    return message_text

async def kommersant_ru_finances():
    year_today = format_date(x2, "yyy", locale='ru')
    mounth_today = format_date(x2, "MM", locale='ru')
    day_today = format_date(x2, "dd", locale='ru')
    # print(year_today,mounth_today,day_today)
                # ДАТА!!!
    URL = 'https://www.kommersant.ru/archive/rubric/40/day/%s-%s-%s' % (year_today, mounth_today, day_today)
    # URL = '''https://www.kommersant.ru/archive/rubric/3/day/2018-06-14?page=2'''  # тест для кнопки "Показать ещё"
    # print(URL)
    xPATH = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_link = '''//a[@class="uho__link uho__link--overlay"]'''
    xPATH_button = '''//*[contains(text(), "Показать еще")]'''

    driver.get(URL)

    # Кнопка "Показать ещё"
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, xPATH_button).click()
    except Exception as e:
        print('kommersant_ru_finances:', e)

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
        link1 = '<a href="%s">kommersant.ru</a>' % link
        link_mass.append(link1)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, link_mass)]
    if message_text == []:
        print('На сайте https://www.kommersant.ru/archive/rubric/40/day нет сегодня новостей!')
    # print(message_text)
    print('kommersant.ru/archive/rubric/40', type(message_text))
    return message_text





# --------------------- ПОТОКИ/ТАЙМЕР -----------------------------
def executeSomething():
    print(AllParseResult)
    asyncio.run(MainParser())
    t = threading.Timer(1800.0, executeSomething)  #600.0
    t.start()

executeSomething()

    # aboba = True
# while aboba == True: