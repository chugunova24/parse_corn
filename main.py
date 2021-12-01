import telebot
import datetime
import os
import re
from telebot import types
from babel.dates import format_date, format_datetime
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
import pprint
import asyncio
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from lxml import etree

# def browser_work():
#     # работа браузера без интерфейса
#     option = Options()
#     option.headless = False
#
#     driver = webdriver.Chrome(options=option)


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
               send = bot.send_message(call.message.chat.id, "Введите слово к которому добавляем синоним.")
               bot.register_next_step_handler(send, AddSynonimTo)
   except Exception as e:
       print(repr(e))

def AddSynonimTo(SynTo):
    global SynToGlobal
    SynToGlobal = ""

    if SynToGlobal.find(' ') != -1:
         send = bot.send_message(SynTo.chat.id, "похоже что вы ввели не одно слово, повторите пожалуйста")
         bot.register_next_step_handler(send, AddSynonimTo)

    SynToGlobal = SynTo.text.lower()
    print(SynToGlobal)
    send = bot.send_message(SynTo.chat.id, "Отлично теперь введите синосим")
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
            print('говно найдено')
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

    # ЧЕРЕЗ SELENIUM

    # url = 'https://zerno.ru/news_list'
    # driver.get(url)
    #
    # xPATH = '''//*[text()='%s']''' % date_today
    # xPATH_link = '''//*[text()='%s']//../../span[2]/span/a''' % date_today
    #
    # # ищет новости на сегодня
    # cell_news_arr = []
    # cell_news = driver.find_elements(By.XPATH, xPATH_link)
    # for i in cell_news:
    #     cell_news_arr.append(i.text)
    #
    # # поиск ссылок
    # news_link_arr = []
    # news_link = driver.find_elements(By.XPATH, xPATH_link)
    # for j in news_link:
    #     a_link = j.get_attribute('href')
    #     news_link_arr.append(a_link)
    #
    # message_text = ["%s %02s" % t for t in zip(cell_news_arr, news_link_arr)]
    # # print(message_text)
    # # for x in message_text:
    # #     bot.send_message(message.chat.id, x)
    #
    # return message_text

    # ЧЕРЕЗ BS4
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
    # bukva = True
    # if bukva == True:
    #     for index:
    #         index =+1
    #         print(dom.xpath(xPATH_link)[index].text)

    # поиск содержимого блоков
    cell_news_arr = []
    for i in range(0, len(count_index)):
        a = dom.xpath(xPATH)[i].text
        cell_news_arr.append(a)
    print(cell_news_arr)
    for x in cell_news_arr:
        bot.send_message(message.chat.id, x)
    # bot.send_message(message.chat.id, cell_news_arr)

    # поиск ссылок на содержимое блоков
    news_link_arr = []
    for i in range(0, len(count_index)):
            a = dom.xpath(xPATH_link)[i]
            news_link_arr.append(a)
    # print(news_link_arr)

    return news_link_arr



# вывод сообщения в чат и zol_ru(message)
async def zol_ru():
    url = 'https://www.zol.ru/news/grain/'
    driver.get(url)

    if datetime.date.today().weekday() == 0:
        yesterday = datetime.datetime.now() - datetime.timedelta(2)
    else:
        yesterday = datetime.datetime.now() - datetime.timedelta(1)

    date_today = format_date(yesterday, "d MMMM yyy", locale='ru')

    xPATH = '''//tr'''
    xPATH_link = '''//tr/td[2]//div/a'''

    cell_news = driver.find_elements(By.XPATH, xPATH)
    cell_news_arr = []
    for cell in cell_news:
        cell_news_arr.append(cell.text)

    # В ПОНЕДЕЛЬНИК МОЖЕТ БЫТЬ ОШИБКА!!kjbjbjnlklmk;l;'
    try:
        index_elem = cell_news_arr.index(date_today)
    except ValueError:
        # bot.send_message(message.chat.id, 'На сайте https://www.zol.ru/ (2) нет сегодня новостей!')
        print('На сайте https://www.zol.ru/ (2) нет сегодня новостей!')
        return

    del cell_news_arr[index_elem:]
    del cell_news_arr[0]

    news_link_arr = []
    news_link = driver.find_elements(By.XPATH, xPATH_link)
    for j in news_link:
        a_link = j.get_attribute('href')
        news_link_arr.append(a_link)
    # print(news_link_arr)
    index_elem -= 1
    del news_link_arr[index_elem:]

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, news_link_arr)]
    return message_text
    # for x in message_text:
    #     bot.send_message(message.chat.id, x)


async def agroinvestor_ru():
    url = 'https://www.agroinvestor.ru/'
    driver.get(url)

    date_today = format_date(x2, "d MMMM yy", locale='ru')
    # date_today = '29 октября 2021'
    xPATH = '''//*[text()='%s']/../../a[2]''' % date_today

    # поиск новостей
    cell_news = driver.find_elements(By.XPATH, xPATH)
    cell_news_arr = []
    for cell in cell_news:
        cell_news_arr.append(cell.text)
    # print(cell_news_arr)

    # поиск ссылок
    news_link_arr = []
    news_link = driver.find_elements(By.XPATH, xPATH)
    for j in news_link:
        a_link = j.get_attribute('href')
        news_link_arr.append(a_link)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, news_link_arr)]
    return message_text
    # for x in message_text:
    #     bot.send_message(message.chat.id, x)


async def agriculture_com():
    url = 'https://www.agriculture.com/search?search_api_views_fulltext=&sort_by=created'
    driver.get(url)

    # date_today = '10.31.2021'
    date_today = format_date(x2, "MM.dd.yyy", locale='ru')
    xPATH = '''//*[contains(text(),'%s')]/../h2''' % date_today
    xPATH_link = '''//*[contains(text(),'%s')]/../h2/a''' % date_today

    # поиск новостей
    cell_news = driver.find_elements(By.XPATH, xPATH)
    cell_news_arr = []
    for cell in cell_news:
        cell_news_arr.append(cell.text)

    # поиск ссылок
    news_link_arr = []
    news_link = driver.find_elements(By.XPATH, xPATH_link)
    for j in news_link:
        a_link = j.get_attribute('href')
        news_link_arr.append(a_link)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, news_link_arr)]
    return message_text
    # for x in message_text:
    #     bot.send_message(message.chat.id, x)


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

    message_words = message.text.lower().split(' ')
    print('\nмеседж ловер')
    try:
        n1 = task1.result()
        n2 = task2.result()
        n3 = task3.result()
        n4 = task4.result()
        a = n1 + n2 + n3 + n4
        # print('ПОЛНЫЙ СПИСОК', a)
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

    # print(WordsLineWithSyn)
    for WordLine in WordsLineWithSyn:
        wordFinded = False
        for word in WordLine.split(" "):
            print(word)
            if wordFinded == False:
                for ParseNews in ParseResult:
                    if ParseNews.lower().replace(':', ' ').replace('.', ' ').replace(',', ' ').replace('"', ' ')\
                            .find(word + " ") != -1:
                        TempParseResult.append(ParseNews)
                        wordFinded = True
        ParseResult = TempParseResult
        TempParseResult = []

    print(ParseResult)

    for elem_r_set in ParseResult:
        bot.send_message(message.chat.id, elem_r_set)



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

