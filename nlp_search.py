# from connect import *
# from main import zerno_ru, zol_ru, driver, bot


# driver = webdriver.Chrome()
# bot = telebot.TeleBot(token)
url = '''https://morpher.ru/Demo.aspx'''
xPATH = '''/html/body/form/table/tbody/tr[4]/td[2]/div/div/table/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/input'''
xPATH_button = '''/html/body/form/table/tbody/tr[4]/td[2]/div/div/table/tbody/tr[2]/td[3]/table/tbody/tr/td[2]/input'''
xPATH_answer = '''//*[contains(@class, 'answer')]'''

@bot.message_handler(commands=['search'])
def redirection(message):
    send  = bot.send_message(message.chat.id, 'Введите ключевое словоsdcss:')
    bot.register_next_step_handler(send, search_news)


def search_news(message):
    message_lower_text = message.text.lower()
    try:
        n1 = zerno_ru()
        n2 = zol_ru()
        a = n1 + n2
        return a
    except Exception:
        print('ОШИБКА ПОИСКА')
    # print('ПОЛНЫЙ СПИСОК', a)
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xPATH))).send_keys(message_lower_text)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xPATH_button))).click()
    info = driver.find_elements(By.XPATH, xPATH_answer)

    b_array = []
    for i in info:
        b_array.append(i.text)
    if '' in b_array:
        b_array.remove('')

    r = []
    # for i in b_array:
    # for j in a:
    #     # print(j)
    #     j = j.lower()
    #     y = re.findall(b_array[0], j)
    #     if not i == '':
    #         r.append(j)


    for i in b_array:
        d = list(filter(i, a))
        print(d)

    print('\n')
    r_set = set(r)
    print(r_set)

    # if not r_set:
    #     bot.send_message(message.chat.id,
    #                      'Результатов не найдено. Попробуйте изменить запрос на прилагательное.')
    # else:
    #     for x in r_set:
    #         bot.send_message(message.chat.id, x)






bot.infinity_polling()
