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
from connect import GetParseResult

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



# -------------- СЛОВАРЬ -----------------
def FindNews(mess):
    asyncio.run(asyncFindNews(mess))
# цикл чтения словаря, для поиска ключевого слова
async def asyncFindNews(message):

    message_words = message.text.lower().split(' ')
    print('\nмеседж ловер')

    f = open('dict.txt', 'r', encoding='utf-8')
    f_lines = f.readlines()

    a = GetParseResult()

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
                    if ParseNews.lower().replace(':', ' ').replace('.', ' ').replace(',', ' ').replace('"', ' ')\
                            .replace('/', ' ').replace('\'', ' ').find(word + " ") != -1:
                        TempParseResult.append(ParseNews)
        ParseResult = TempParseResult
        TempParseResult = []

    ParseResult = set(ParseResult)
    # print(ParseResult)

    for elem_r_set in ParseResult:
        # bot.send_message(message.chat.id, elem_r_set)
        bot.send_message(message.chat.id, elem_r_set, disable_web_page_preview=True, parse_mode='html')



# ----------------------- ЗАПУСК -------------------------

bot.infinity_polling()
