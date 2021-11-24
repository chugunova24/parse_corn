import telebot
import datetime
import os
import re
from telebot import types
from babel.dates import format_date, format_datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pprint

# работа браузера без интерфейса
option = Options()
option.headless = False

driver = webdriver.Chrome(options=option)

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
    button1 = types.InlineKeyboardButton(text="Сайт 1", callback_data="Site1")
    button2 = types.InlineKeyboardButton(text="Сайт 2", callback_data="Site2")
    button3 = types.InlineKeyboardButton(text="Сайт 3", callback_data="Site3")
    button4 = types.InlineKeyboardButton(text="Сайт 4", callback_data="Site4")
    button5 = types.InlineKeyboardButton(text="Поиск", callback_data="FindByWord")
    button6 = types.InlineKeyboardButton(text="Добавить синоним", callback_data="AddSynonim")
    markup.add(button1).add(button2).add(button3).add(button4).add(button5).add(button6)
    bot.send_message(message.chat.id,
                     "Здесь ты можешь выбрать с какого сайта посмотреть новости, или найти новость по ключевому слову. Добавление синонимов улучшает качество поиска!",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
   try:
       if call.message:
           if call.data == "Menue":
               MainMenue(call.message)
           if call.data == "Site1":
               zerno_ru()
           if call.data == "Site2":
               zol_ru()
           if call.data == "Site3":
               agroinvestor_ru()
           if call.data == "Site4":
               agriculture_com()
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

def zerno_ru():
    url = 'https://zerno.ru/news_list'
    driver.get(url)

    xPATH = '''//*[text()='%s']''' % date_today
    xPATH_link = '''//*[text()='%s']//../../span[2]/span/a''' % date_today

    # ищет новости на сегодня
    cell_news_arr = []
    cell_news = driver.find_elements(By.XPATH, xPATH_link)
    for i in cell_news:
        cell_news_arr.append(i.text)

    # поиск ссылок
    news_link_arr = []
    news_link = driver.find_elements(By.XPATH, xPATH_link)
    for j in news_link:
        a_link = j.get_attribute('href')
        news_link_arr.append(a_link)

    message_text = ["%s %02s" % t for t in zip(cell_news_arr, news_link_arr)]
    # print(message_text)
    # for x in message_text:
    #     bot.send_message(message.chat.id, x)

    return message_text


# вывод сообщения в чат и zol_ru(message)
def zol_ru(message):
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
        bot.send_message(message.chat.id, 'На сайте https://www.zol.ru/ (2) нет сегодня новостей!')
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


def agroinvestor_ru():
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


def agriculture_com():
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


# цикл чтения словаря, для поиска ключевого слова
def FindNews(message):
    message_lower_text = message.text.lower()
    print('\nмеседж ловер')
    try:
        n1 = zerno_ru()
        n2 = zol_ru()
        a = n1 + n2
        # print('ПОЛНЫЙ СПИСОК', a)
    except Exception:
       print('ОШИБКА ПОИСКА')

    key = f'{message_lower_text} '
    print('\nключ найден')
    f = open('dict.txt', 'r', encoding='utf-8')
    f_lines = f.readlines()

    txt_line = ""
    for line in f_lines:
        print(line)
        print(key)
        if line.find(key) != -1:
            txt_line = line.split(' ')
            print('говно найдено', txt_line)
    if not txt_line:
        bot.send_message(message.chat.id, '')

    # print('\nстроки прочитаны')
    # поиск в файле строки с нужным набором слов (выход str)

    result = []
    for str_a in a:
        bul_p = False
        for word in txt_line:
            print(word)
            if bul_p == False:
                if str_a.find(word + ' ') != -1:
                    result.append(str_a)
                    bul_p = True



    print('\nрезультат итоговый')
    r_set = set(result)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(r_set)


bot.infinity_polling()


#------------------------------МУСОР ЕБАНЫЙ---------------------------------


@bot.message_handler(commands=['Find_By_Word'])
def answer(message):
    send = bot.send_message(message.chat.id, '''Выберите номер сайта:\b
            zerno.ru = 1
            zol.ru = 2
            agroinvestor.ru = 3
            agriculture.com = 4
            ПОИСК = '5'
            ''')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,row_width=2)
    button1 = types.KeyboardButton(" Привет")
    button2 = types.KeyboardButton(" Как дела?")
    markup.add(button1,button2)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup=markup)
    bot.register_next_step_handler(send, get_news)


def get_news(message):
    a = message.text
    if a == '1':
        zerno_ru(message)
    elif a == '2':
        zol_ru(message)
    elif a == '3':
        agroinvestor_ru(message)
    elif a == '4':
        agriculture_com(message)
    elif a == '5':
        send = bot.send_message(message.chat.id, '''Введите ключевое слово:''')
        bot.register_next_step_handler(send, FindNews)
    else:
        bot.send_message(message.chat.id, '''Мы не нашли номер, введите заново.''')

