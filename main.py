import telebot
import datetime
import re
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


# последовательность
@bot.message_handler(commands=['news_today'])
def answer(message):
    send = bot.send_message(message.chat.id, '''Выберите номер сайта:\b
            zerno.ru = 1
            zol.ru = 2
            agroinvestor.ru = 3
            agriculture.com = 4
            ПОИСК = '5'
            ''')
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
        bot.register_next_step_handler(send, read_txt)
    else:
        bot.send_message(message.chat.id, '''Мы не нашли номер, введите заново.''')


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
def zol_ru():
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


# добавление ключевого слова
def dict_new_word(message):
    f = open('dict.txt', 'a', encoding='utf-8')
    word = 'бляьб1111'
    f.write('\n')
    f.write(word + ' ')
    f.close


# добавление синонимов к ключевому слову
def synonym(message):
    f = open('dict.txt', 'a', encoding='utf-8')
    word = ['сука', 'ааа', 'нееееет']
    for elem in word:
        f.write(elem + ' ')
    f.close


# чтение последней строки, чтобы показать результат запроса
def print_last_line(message):
    f = open('dict.txt', 'r', encoding='utf-8')
    last_line = f.readlines()[-1]
    f.close
    return last_line


# цикл чтения словаря, для поиска ключевого слова
def read_txt(message):
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
