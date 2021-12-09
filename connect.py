import datetime
import sched, time
from babel.dates import format_date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import threading


# работа браузера без интерфейса
option = Options()
option.headless = True

driver = webdriver.Chrome(options=option)
driver.set_window_size(1920, 1080)

x = datetime.datetime.today()
x2 = datetime.datetime.date(x)
date_today = format_date(x2, locale='de_DE')

def forbes_ru():
    # date_today = '03.12.2021'


    URL = 'https://www.forbes.ru/'
    xPATH = '''//ul[@data-interval="%s"]/li/a/div[@class="Tt2J2"]''' %date_today
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
    print('ЗАВЕРШЕНО')

    # driver.quit()

    return forbes_massive

def executeSomething():
    forbes_ru()
    time.sleep(60)

aboba = True
while aboba == True:
    executeSomething()