import telebot
from telebot import types
import datetime
import os
from babel.dates import format_date, format_datetime
import pprint
import asyncio
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from lxml import etree
import re
from connect import forbes_ru

# # работа браузера без интерфейса
# option = Options()
# option.headless = False
#
# driver = webdriver.Chrome(options=option)

TOKEN = '2016761889:AAF0Baan6ouhKLwClb0O4utKv47wnclaZEA'
bot = telebot.TeleBot(TOKEN)

x = datetime.datetime.today()
x2 = datetime.datetime.date(x)
date_today = format_date(x2, locale='de_DE')


# InlineKeyboardMarkup - кнопки привязаны к тексту
# ReplyKeyboardMarkup - кнопки находятся под чатом
# InlineKeyboardButton - кнопка в чате
# KeyboardButton - кнопка под вводом текста
# (one_time_keyboard=True) - убирать кнопки после нажатия

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет новичок! Я новостной бот. :)")
    MainMenue(message)

def MainMenue(message):
    markup = types.InlineKeyboardMarkup()
    # button1 = types.InlineKeyboardButton(text="Сайт 1", callback_data="Site1")
    # button2 = types.InlineKeyboardButton(text="Сайт 2", callback_data="Site2")
    # button3 = types.InlineKeyboardButton(text="Сайт 3", callback_data="Site3")
    # button4 = types.InlineKeyboardButton(text="Сайт 4", callback_data="Site4")
    button5 = types.InlineKeyboardButton(text="Поиск", callback_data="FindByWord")
    button6 = types.InlineKeyboardButton(text="Добавить синоним", callback_data="AddSynonim")
    markup.add(button5).add(button6)
    bot.send_message(message.chat.id,
                     "Здесь Вы можете найти новость по ключевому слову. Добавление синонимов улучшает качество поиска!",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
   try:
       if call.message:
           if call.data == "Menue":
               MainMenue(call.message)
           # if call.data == "Site1":
           #     zerno_ru()
           # if call.data == "Site2":
           #     zol_ru()
           # if call.data == "Site3":
           #     agroinvestor_ru()
           # if call.data == "Site4":
           #     agriculture_com()
           if call.data == "FindByWord":
               bot.send_message(call.message.chat.id, "Введите слово для поиска.")
               bot.register_next_step_handler(call.message, FindNews)
           if call.data == "AddSynonim":
               send = bot.send_message(call.message.chat.id, "Введите слово, к которому добавляем синоним.")
               bot.register_next_step_handler(send, AddSynonimTo)
   except Exception as e:
       print(repr(e))

def AddSynonimTo(SynTo):
    global SynToGlobal
    SynToGlobal = ""

    if SynToGlobal.find(' ') != -1:
         send = bot.send_message(SynTo.chat.id, "Похоже, что вы ввели не одно слово, повторите пожалуйста")
         bot.register_next_step_handler(send, AddSynonimTo)

    SynToGlobal = SynTo.text.lower()
    print(SynToGlobal)
    send = bot.send_message(SynTo.chat.id, "Отлично, теперь введите синосим")
    bot.register_next_step_handler(send, AddSynonimWord)

def AddSynonimWord(SynWord):
    f = open('dict.txt', 'r', encoding='utf-8')
    f_lines = f.readlines()
    f.close()

    os.system(r'nul>file.txt')

    f = open('dict.txt', 'w', encoding='utf-8')
    HavWordToSyn = False
    DoubleSyn = False
    SynWordText = SynWord.text.lower()
    for line in f_lines:
        if line.find(SynWordText) != -1:
            DoubleSyn = True

        if line.find(SynToGlobal) != -1:
            if DoubleSyn == False:
                f.write(line + " " + SynWordText)
            else:
                f.write(line)
            print('строка в словаре найдена')
            HavWordToSyn = True
        else:
            f.write(line)

    if DoubleSyn == False:
        if HavWordToSyn == False:
            bot.send_message(SynWord.chat.id, "слово не найдено, добавляем.")
            if(f_lines.count("\n") == 1):
                f.write("\n")
            f.write(SynToGlobal + " " + SynWordText)
        bot.send_message(SynWord.chat.id, "Слово успешно добавлено.")
    else:
        bot.send_message(SynWord.chat.id, "Введенный вами синоним уже есть в списке")

    markup = types.InlineKeyboardMarkup()
    GoBack = types.InlineKeyboardButton(text="Назад", callback_data="Menue")
    Write = types.InlineKeyboardButton(text="Повторить", callback_data="AddSynonim")
    markup.add(GoBack,Write)
    bot.send_message(SynWord.chat.id, "Вернуться назад, или повторить",reply_markup=markup)


# -------------- ПАРСЕР -----------------
# @bot.message_handler(commands='z1')
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
        print(link1)
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


def apk_inform_com():
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
    # print(message_text)

    # for x in message_text:
    #     bot.send_message(message.chat.id, x, disable_web_page_preview=True, parse_mode='html')




# НЕ ДОДЕЛАН!!!!!!!!!!!!!
def ria_ru():
    URL = '''https://ria.ru/search/?query='''

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





# def forbes_ru():
#     URL = '''https://www.forbes.ru/'''
#
#     xPATH ='''//ul[@data-interval="08.12.2021"]/li/a/div[@class="Tt2J2"]'''
#     xPATH_link = '''//*[contains(text(),'Сегодня')]/../../../../..//a[@class='text']/@href'''
#
#
#     webpage = requests.get(URL, stream=True, timeout=(20, 100))
#     soup = BeautifulSoup(webpage.content, "html.parser")
#     dom = etree.HTML(str(soup))
#     count_index = dom.xpath(xPATH)
#     # count_index = len(count_index)
#     print(soup)
#
#     # поиск содержимого блоков НА 1 СТРАНИЦЕ
#     cell_news_arr = []
#     for i in range(0, len(count_index)):
#         a = dom.xpath(xPATH)[i].text
#         cell_news_arr.append(a)
#     print(cell_news_arr)
#
#     # # поиск ссылок на содержимое блоков
#     # news_link_arr = []
#     # for i in range(0, len(count_index)):
#     #     a = dom.xpath(xPATH_link)[i]
#     #     first_part_link = 'https://www.apk-inform.com'
#     #     a = first_part_link + a
#     #     news_link_arr.append(a)
#     # # print(news_link_arr)
#


# -------------- СЛОВАРЬ -----------------
def FindNews(mess):
    asyncio.run(asyncFindNews(mess))
# цикл чтения словаря, для поиска ключевого слова
async def asyncFindNews(message):
    task1 = asyncio.create_task(zerno_ru())
    task2 = asyncio.create_task(zol_ru())
    task3 = asyncio.create_task(agroinvestor_ru())
    task4 = asyncio.create_task(agriculture_com())
    await asyncio.wait([task1,task2,task3,task4])
    # await asyncio.wait([task1])

    message_words = message.text.lower().split(' ')
    print('\nмеседж ловер')
    try:
        n1 = task1.result()
        n2 = task2.result()
        n3 = task3.result()
        n4 = task4.result()
        a = n1 + n2 + n3 + n4
        # a = n1 + n2
        print('ПОЛНЫЙ СПИСОК', a)
    except Exception:
       print('ОШИБКА ПОИСКА')

    f = open('dict.txt', 'r', encoding='utf-8')
    f_lines = f.readlines()


    WordsLineWithSyn = []
    for Word in message_words:
        WordWasFind = False
        for line in f_lines:
            # print(line)
            if WordWasFind == False:
                if line.find(Word + " ") != -1:
                    WordsLineWithSyn.append(line)
                    print('слово найдено', Word)
                    WordWasFind = True
        if WordWasFind == False:
            WordsLineWithSyn.append(Word)

    # print('\nстроки прочитаны')
    # поиск в файле строки с нужным набором слов (выход str)

    ParseResult = a
    TempParseResult = []

    # print("ParseResult")
    # print(ParseResult)
    for WordLine in WordsLineWithSyn:
        for word in WordLine.split(" "):
                for ParseNews in ParseResult:
                    if ParseNews.lower().replace(':', ' ').replace('.', ' ').replace(',', ' ').replace('"', ' ').replace('/', ' ')\
                            .find(word + " ") != -1:
                        TempParseResult.append(ParseNews)
        ParseResult = TempParseResult
        TempParseResult = []

    ParseResult = set(ParseResult)
    # print(ParseResult)

    for elem_r_set in ParseResult:
        # bot.send_message(message.chat.id, elem_r_set)
        bot.send_message(message.chat.id, elem_r_set, disable_web_page_preview=True, parse_mode='html')





bot.infinity_polling()


#------------------------------ МУСОР ---------------------------------


# @bot.message_handler(commands=['Find_By_Word'])
# def answer(message):
#     send = bot.send_message(message.chat.id, '''Выберите номер сайта:\b
#             zerno.ru = 1
#             zol.ru = 2
#             agroinvestor.ru = 3
#             agriculture.com = 4
#             ПОИСК = '5'
#             ''')
#
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,row_width=2)
#     button1 = types.KeyboardButton(" Привет")
#     button2 = types.KeyboardButton(" Как дела?")
#     markup.add(button1,button2)
#     bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup=markup)
#     bot.register_next_step_handler(send, get_news)
#
#
# def get_news(message):
#     a = message.text
#     if a == '1':
#         zerno_ru(message)
#     elif a == '2':
#         zol_ru(message)
#     elif a == '3':
#         agroinvestor_ru(message)
#     elif a == '4':
#         agriculture_com(message)
#     elif a == '5':
#         send = bot.send_message(message.chat.id, '''Введите ключевое слово:''')
#         bot.register_next_step_handler(send, FindNews)
#     else:
#         bot.send_message(message.chat.id, '''Мы не нашли номер, введите заново.''')

