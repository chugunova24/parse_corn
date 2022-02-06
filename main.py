import telebot
from telebot import types
import datetime
# import os
from babel.dates import format_date, format_datetime
# import pprint
import time
from threading import Timer
import asyncio
import pymorphy2
from lemminflect import getInflection, getAllInflections
# from bs4 import BeautifulSoup
# import requests
# from urllib.request import urlopen
# from lxml import etree
import re
# from connect import GetParseResult

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

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.send_message(message.chat.id, "Привет новичок! Я новостной бот. :)")
#     MainMenue(message)


@bot.message_handler(commands=['help'])
def infoBot(message):
    bot.send_message(message.chat.id,
                     "<i>Информация о боте</i>.\n\n"
                     "<b>1) Что делает бот?</b>\n"
                     f"   - Данный бот отправляет агроновости за сегодняшний день ({date_today}).\n"
                     "     Чтобы начать поиск введите команду /start, а затем выберите кнопку 'Поиск'"
                     " и следуйте инструкции.\n\n"
                     "<b>2) Что такое ключевое слово?</b>\n"
                     "   - Ключевое слово позволяет искать новости по конкретному слову.\n"
                     "     Чтобы добавить ключевое слово введите команду /start, а затем выберите кнопку 'Добавить ключевое слово'"
                     " и следуйте инструкции.\n\n"
                     "<b>3) Что такое синоним?</b>\n"
                     "   - Синонимы добавляются к ключевому слову. Они улучшают качество поиска, т.е. он становится более точным.\n"
                     "     Чтобы добавить синоним  введите команду /start, а затем выберите кнопку 'Добавить синоним'"
                     " и следуйте инструкции.\n\n"
                     "<b>4) Как посмотреть какие ключевые слова добавлены в словарь?</b>\n"
                     "- Чтобы заглянуть в словарь, введите команду /dict.\n"
                     "Бот выгрузит словарь в чат, а Вы сможете его скачать и просмотреть.\n\n"
                     "<b>5) А что если мне надо посмотреть только на конкретную строчку в словаре?</b>\n"
                     "- Не проблема. Введите команду /start, потом выберите кнопку 'Словарь', а затем кнопку 'Найти строку в словаре' и следуйте инструкции.\n\n\n\n"
                     "<i>Рекомендации.</i>\n\n"
                     "<b>Собираетесь добавить ключевое слово или синоним?</b>\n"
                     "Если Вы хотите воспользоваться автогенерацией синонимов (похожих слов), то рекомендуем вводить свое слово в начальной форме.\n"
                     "Начальная форма существительного: именительный падеж + единственное число (зерно, ячмень, соя).\n"
                     "Начальная форма прилагательного: мужской род + именительный падеж + единственное число (зерновой, ячменный, соевый).\n"
                     "Начальная форма глагола: Что делать? (дремать).\n\n"
                     "<b>Хороший пример:</b>\n"
                     "бот: Введите ключевое слово, которое хотите добавить в словарь.\n"
                     "Вы: зерно\n"
                     "бот: Добавить к слову зерно следующие синонимы? Предпросмотр: <strong>зерно зерна зерну зерном зерне зёрна зёрен зёрнам зёрна зёрнами зёрнах</strong>. Напишите боту 'да' или 'нет'.\n"
                     "<i>(#комментарий: если ответить 'да', то вместе с ключевым словом будут добавлены сгенерированные синонимы, если ответить 'нет', то будет добавлено только ключевое слово.)</i>"
                     "Вы: да\n\n"
                     "<i>(#комментарий: после добавления ключевого слова 'зерно' + сгенерированных синонимов, рекомендую добавить его прилагательное. К именам существительным генерируются синонимы-существительные, к именам прилагательным генерируются синонимы-прилагательные, к глаголам генерируются синонимы-глаголы)</i>\n"
                     "бот: Введите ключевое слово, к которому хотите добавить синоним.\n"
                     "Вы: зерно\n"
                     "бот: Отлично, теперь введите синосим.\n"
                     "Вы: зерновой\n"
                     "бот: Добавить к синониму зерновой похожие слова? Предпросмотр: <strong>зерновой зернового зерновому зернового зерновой зерновым зерновом зерновая зерновой зерновой зерновую зерновой зерновою зерновой зерновое зернового зерновому зерновое зерновым зерновом зерновые зерновых зерновым зерновых зерновые зерновыми зерновых зерновее зерновей позерновее позерновей</strong>. Напишите боту 'да' или 'нет'.\n"
                     "Вы: да\n\n"
                     "<i>Готово! Теперь строчка с ключевым словом 'зерно' выглядит в словаре вот так: <strong>зерно зерна зерну зерном зерне зёрна зёрен зёрнам зёрна зёрнами зёрнах зерновой зернового зерновому зернового зерновой зерновым зерновом зерновая зерновой зерновой зерновую зерновой зерновою зерновой зерновое зернового зерновому зерновое зерновым зерновом зерновые зерновых зерновым зерновых зерновые зерновыми зерновых зерновее зерновей позерновее позерновей</strong></i>\n"
                     ""
                     "", parse_mode="html")


# ================ МЕНЮ ===================
@bot.message_handler(commands=['start'])
def MainMenue(message):
    markup = types.InlineKeyboardMarkup()
    button5 = types.InlineKeyboardButton(text="Поиск 🔎", callback_data="FindByWord")
    button6 = types.InlineKeyboardButton(text="Добавить синоним ✔", callback_data="AddSynonim")
    button7 = types.InlineKeyboardButton(text="Добавить ключевое слово ✔", callback_data="AddKeyWordCALL")
    button8 = types.InlineKeyboardButton(text="Словарь 📄", callback_data="DictList")
    markup.add(button5).add(button6).add(button7).add(button8)
    bot.send_message(message.chat.id,
                     "Здесь Вы можете найти новость по ключевому слову.",
                     reply_markup=markup)



# ---------------------- ОБРАБОТКА CALL.DATA --------------------------------------------

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "Menue":
               MainMenue(call.message)
               bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Menue", reply_markup=None)

            if call.data == "FindByWord":
               bot.send_message(call.message.chat.id, "Введите слово для поиска.\n"
                                                      "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
               bot.register_next_step_handler(call.message, FindNews)
               bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Поиск 🔎", reply_markup=None)

            if call.data == "AddSynonim":
               send = bot.send_message(call.message.chat.id, "Введите ключевое слово, к которому хотите добавить синоним.\n"
                                                             "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
               bot.register_next_step_handler(send, AddSynonimTo)
               bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Добавить синоним ✔", reply_markup=None)

            if call.data == "AddKeyWordCALL":
               send = bot.send_message(call.message.chat.id, "Введите ключевое слово, которое хотите добавить в словарь.\n"
                                                             "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
               bot.register_next_step_handler(send, AddKeyWord)
               bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Добавить ключевое слово ✔", reply_markup=None)

            if call.data == "DictList":
                markup = types.InlineKeyboardMarkup()
                bttn1 = types.InlineKeyboardButton(text="Удалить ключевое слово ❌", callback_data="delKeyW")
                bttn2 = types.InlineKeyboardButton(text="Удалить синоним ❌", callback_data="delSynW")
                bttn3 = types.InlineKeyboardButton(text="Найти строку в словаре ☰", callback_data="FindString")
                # bttn4 = types.InlineKeyboardButton(text="Добавить ключевое слово", callback_data="AddKeyWordCALL")
                markup.add(bttn1).add(bttn2).add(bttn3)
                bot.send_message(call.message.chat.id, "Выберите действие со словарем.", reply_markup=markup)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Словарь 📄", reply_markup=None)

            if call.data == "delKeyW":
               send = bot.send_message(call.message.chat.id,
                                       "<strong>Внимание: вместе с ключевым словом удаляются все его синонимы.</strong>\n"
                                       "Введите ключевое слово, которое требуется удалить.\n"
                                       "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
               bot.register_next_step_handler(send, delKeyWord)
               bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удалить ключевое слово ❌", reply_markup=None)

            if call.data == "delSynW":
               send = bot.send_message(call.message.chat.id,
                                       "Введите ключевое слово, синоним которого собираетесь удалить.\n"
                                       "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
               bot.register_next_step_handler(send, delSynWord)
               bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удалить синоним ❌", reply_markup=None)

            if call.data == "FindString":
                send = bot.send_message(call.message.chat.id,
                                        "Введите ключевое слово (по нему мы будем искать строчку в словаре).\n"
                                        "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.",
                                        parse_mode="html")
                bot.register_next_step_handler(send, FindingString)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Найти строку в словаре ☰", reply_markup=None)

            # if call.data == "addAutoGen":
            #     send = bot.send_message(call.message.chat.id, "Хорошо, ща сделаем")
            #     bot.register_next_step_handler(send, auto_generation_word)
            #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Сгенерировать синонимы?", reply_markup=None)
            # if call.data == "NotaddAutoGen":
            #     send = bot.send_message(call.message.chat.id, "Ладно, не будем делать")
            #     bot.register_next_step_handler(send, auto_generation_word)
            #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Сгенерировать синонимы?", reply_markup=None)
    except Exception as e:
        print(repr(e))
    # UnloadDict



# -------------------- УДАЛЕНИЕ СИНОНИМА И КЛЮЧЕВОГО СЛОВА ------------------------------

def delKeyWord(message):
    KeyWordText = message.text.lower()

    f = open('dict.txt', 'r', encoding='utf-8')
    f_lines = f.readlines()
    f.close()

    if KeyWordText == 'стоп':
        return bot.send_message(message.chat.id, 'Процесс остановлен.')

    # проверка существует ли ключевое слово в словаре
    check = 0
    HaveKey = False
    for line in f_lines:
        line = line.replace('\n', '')
        words = line.split(' ')
        for word in words:
            if words[0] == KeyWordText:
                line = line + '\n'
                indxLine = f_lines.index(line)
                # print(indxLine)
                HaveKey = True
                check+=1
                break
    # print(check)
    # print(HaveKey)
    if HaveKey == False:
        bot.send_message(message.chat.id, "Такое ключевое слово в словаре не найдено.")
    else:
        del f_lines[indxLine]
        f = open('dict.txt', 'w', encoding='utf-8')
        for line in f_lines:
            f.write(line)
        bot.send_message(message.chat.id, f"Ключевое слово <strong>{KeyWordText}</strong> и его синонимы успешно удалены.", parse_mode="html")
        f.close()

def delSynWord(message):
    # удаление синонима из строки
    def delSyn(message):
        SynText = message.text.lower()

        if SynText == 'стоп':
            return bot.send_message(message.chat.id, 'Процесс остановлен.')

        f = open('dict.txt', 'w', encoding='utf-8')
        HaveSyn = False
        # проверка существования синонима
        for line in f_lines:
            line1 = line.replace('\n', '')
            words = line1.split(' ')
            for word in words:
                if words[0] != word:
                    if word == SynText:
                        HaveSyn = True
                        break
        if HaveSyn == False:
            for line in f_lines:
                f.write(line)
            send = bot.send_message(message.chat.id, "Такого синонима не найдено. Повторите ещё раз.\n"
                                                     f"Содержание строки: <strong>{f_lines[indxLine]}</strong>.\n"
                                                     "Для отмены процесса напишите слово <strong><u>'стоп'</u></strong>.", parse_mode="html")
            bot.register_next_step_handler(send, delSyn)
        # удаление синонима ЕСЛИ ОН НЕ ИНД[0]
        if HaveSyn == True:
            ln = f_lines[indxLine].replace('\n', '')
            line_words = ln.split(' ')
            if line_words[0] != SynText:
                indx_SynText = line_words.index(SynText)
                # NewStr = f_lines[indxLine].replace(f'{SynText}', '')
                del line_words[indx_SynText]
                line_words[-1] += '\n'
                # print(line_words)
                NewStr = ' '.join(line_words)
                f_lines[indxLine] = NewStr
                for line in f_lines:
                    f.write(line)
        if HaveSyn == True:
            n_s = f_lines[indxLine].split(' ')
            keyWord = n_s[0]
            bot.send_message(message.chat.id, f"Синоним <strong>{SynText}</strong> успешно удален из ключевого слова <strong>{keyWord}</strong>.",
                                              parse_mode="html")
        f.close()


    # проверка
    KeyText = message.text.lower()

    if KeyText == 'стоп':
        return bot.send_message(message.chat.id, 'Процесс остановлен.')

    f = open('dict.txt', 'r', encoding='utf-8')
    f_lines = f.readlines()
    f.close()

    # проверка существует ли ключевое слово в словаре
    HaveKey = False
    for line in f_lines:
        words = line.split(' ')
        # print(words)
        if words[0] == KeyText:
            indxLine = f_lines.index(line)
            # print(indxLine)
            HaveKey = True
            break

    # print(check)
    # print(HaveKey)
    if HaveKey == False:
        send = bot.send_message(message.chat.id, "Такое ключевое слово в словаре не найдено. Повторите ещё раз.\n"
                                                 "Для отмены процесса напишите слово <strong><u>'стоп'</u></strong>.", parse_mode="html")
        bot.register_next_step_handler(send, delSynWord)
    # передача синонима в следующую функцию
    else:
        send = bot.send_message(message.chat.id, f"Отлично, введите синоним, который хотите удалить из ключевого слова <strong>{KeyText}</strong>.\n"
                                                 f"Содержание строки: <strong>{f_lines[indxLine]}</strong>\n"
                                                 "Для отмены процесса напишите слово <strong><u>'стоп'</u></strong>.", parse_mode="html")
        bot.register_next_step_handler(send, delSyn)






# -------------------- ДОБАВЛЕНИЕ СИНОНИМА И КЛЮЧЕВОГО СЛОВА ------------------------------

# def auto_generation_word(message):
#     textUser = message.text.lower()


# разбор ключевого слова, проверка на второе слово, передача слова
# добавление ключевого слова в словарь
def AddKeyWord(message):
    # добавление ключевого слова в словарь
    def AddWord():
        WordText = WordToGlobal.lower()
        # print(WordText)

        if WordText == 'стоп':
            return bot.send_message(message.chat.id, 'Процесс остановлен.')

        f = open('dict.txt', 'r', encoding='utf-8')
        f_lines = f.readlines()
        # print(f_lines)
        f.close()

        # f = open('dict.txt', 'a+', encoding='utf-8')
        # with open('dict.txt', 'a+', encoding='utf-8') as f:
        # дубль слова
        DoubleSyn = False
        for line in f_lines:
            line = line.replace('\n', '')
            words_in_line = line.split(' ')
            if words_in_line[0] == WordText:
                DoubleSyn = True
                send = bot.send_message(message.chat.id, "Такое ключевое слово уже существует. Попробуйте ещё раз.\n"
                                                         "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.",
                                        parse_mode="html")
                bot.register_next_step_handler(send, AddKeyWord)
                break

        # print(DoubleSyn)
        if DoubleSyn == False:
            # markup = types.InlineKeyboardMarkup()
            # bttn1 = types.InlineKeyboardButton(text="Да, добавить", callback_data="addAutoGen")
            # bttn2 = types.InlineKeyboardButton(text="Нет", callback_data="NotaddAutoGen")
            # markup.add(bttn1).add(bttn2)
            # send = bot.send_message(message.chat.id, f"Добавить к слову <strong>{WordText}</strong> синонимы автоматически?")
            # bot.register_next_step_handler(send, auto_generation_word)
            def congrat():
                markup = types.InlineKeyboardMarkup()
                GoBack = types.InlineKeyboardButton(text="Назад в меню", callback_data="Menue")
                Write = types.InlineKeyboardButton(text="Повторить", callback_data="AddKeyWordCALL")
                markup.add(GoBack, Write)
                bot.send_message(message.chat.id, "Вернуться назад, или повторить", reply_markup=markup)

            def answerAuto(message):
                textUser = message.text.lower()
                if textUser == 'стоп':
                    return bot.send_message(message.chat.id, 'Процесс остановлен.')
                if textUser == 'да':
                    f = open('dict.txt', 'a+', encoding='utf-8')
                    wordK = f.write(nlp_result)
                    bot.send_message(message.chat.id, f"Ключевое слово с синонимами: <strong>{nlp_result}</strong> успешно добавлено.", parse_mode="html")
                    f.close()
                    congrat()
                elif textUser == 'нет':
                    f = open('dict.txt', 'a+', encoding='utf-8')
                    wordK = f.write(str(WordText) + "\n")  # старое
                    bot.send_message(message.chat.id, f"Ключевое слово <strong>{WordText}</strong> успешно добавлено.", parse_mode="html")
                    f.close()
                    congrat()
                else:
                    questionAuto()

            # wordK = str(WordText) + "\n" # старое
            # print(wordK)

            nlp_result = NLP_CASE(WordText)
            nlp_result = nlp_result.replace('\n', '')
            new_nlp = nlp_result.split(' ')
            for n in new_nlp:
                if n == WordText:
                    del new_nlp[new_nlp.index(n)]
            # new_nlp = set(new_nlp) # плохая идея
            # block = []
            # for x in new_nlp:
            #     block.append(x)
            # # print(block)
            new_nlp.insert(0, WordText)
            nlp_result = ' '.join(new_nlp) + '\n'
            # print(nlp_result)

            def questionAuto():
                send = bot.send_message(message.chat.id,
                                        f"Добавить к слову <strong>{WordText}</strong> следующие синонимы?\n"
                                        f"Предпросмотр: <strong>{nlp_result}</strong>\n"
                                        f"Напишите боту <strong>'да'</strong> или <strong>'нет'</strong>.\n"
                                        f"Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.",
                                        parse_mode="html")
                bot.register_next_step_handler(send, answerAuto)
            questionAuto()

            # wordK = f.write(NLP_CASE(WordText))
            # bot.send_message(message.chat.id, f"Ключевое слово {WordText} успешно добавлено.")

    # global WordToGlobal
    # WordToGlobal = ""
    WordToGlobal = message.text.lower()

    if WordToGlobal.find(' ') != -1:
         send = bot.send_message(message.chat.id, "Похоже, что вы ввели не одно слово. Ключевое слово должно содержать одно слово.\n"
                                                  "Введите ещё раз.\n"
                                                  "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
         bot.register_next_step_handler(send, AddKeyWord)
    else:
        AddWord()



# # разбор слова-синонима, проверка на второе слово, передача слова
# # добавление синонима в словарь
def AddSynonimTo(message):

    # добавление синонима в словарь
    def AddSynonimWord(message):

        # человек ввел новый синоним
        SynWordText = message.text.lower()

        if SynWordText.find(' ') != -1:
            send = bot.send_message(message.chat.id, "Похоже, что вы ввели не одно слово, повторите пожалуйста\n"
                                                     "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.",
                                                     parse_mode="html")
            return bot.register_next_step_handler(send, AddSynonimTo)

        # f = open('dict.txt', 'w', encoding='utf-8')

        # стоп-слово
        if SynWordText == 'стоп':
            for line in f_lines:
                f.write(line)
            return bot.send_message(message.chat.id, 'Процесс остановлен.')

        # f = open('dict.txt', 'a+', encoding='utf-8')
        # f = open('dict.txt', 'w', encoding='utf-8')
        # HavWordToSyn = False
        # DoubleSyn = False

        DoubleSyn = False
        for line in f_lines:
            if line.find(SynWordText+' ') != -1:
                DoubleSyn = True
                bot.send_message(message.chat.id, f"Синоним <strong>{SynWordText}</strong> уже есть в словаре.", parse_mode="html")
                break
                # for line in f_lines:
                #     f.write(line)

        if DoubleSyn == False:
            # inStr = f_lines[indexLINE]
            # # print('index:', inStr)
            # NewStr = inStr.replace('\n', f' {NLP_CASE(SynWordText)}\n')
            # # print(NewStr)
            # f_lines[indexLINE] = NewStr
            # # print(f_lines)
            # for line in f_lines:
            #     f.write(line)
            # bot.send_message(message.chat.id, f"Синоним {SynWordText} успешно добавлен.")


            def answerAuto2(message):
                textUser = message.text.lower()
                if textUser == 'стоп':
                    return bot.send_message(message.chat.id, 'Процесс остановлен.')
                if textUser == 'да':
                    f = open('dict.txt', 'w', encoding='utf-8')
                    indStr = f_lines[indexLINE]
                    NewStr = indStr.replace('\n', f' {NLP_CASE(SynWordText)}')
                    f_lines[indexLINE] = NewStr
                    for line in f_lines:
                        f.write(line)
                    f.close()
                    # wordK = f.write(NLP_CASE(SynWordText))
                    bot.send_message(message.chat.id, f"Синонимы:\n<strong>{nlp_result}</strong>\nуспешно добавлены к ключевому слову <strong>{SynToGlobal}</strong>.", parse_mode="html")
                    congrat()
                elif textUser == 'нет':
                    f = open('dict.txt', 'w', encoding='utf-8')
                    indStr = f_lines[indexLINE]
                    NewStr = indStr.replace('\n', f' {SynWordText}\n')
                    f_lines[indexLINE] = NewStr
                    for line in f_lines:
                        f.write(line)
                    f.close()
                    bot.send_message(message.chat.id, f"Синоним <strong>{SynWordText}</strong> успешно добавлен к ключевому слову <strong>{SynToGlobal}</strong>.", parse_mode="html")
                    congrat()
                else:
                    questionAuto2()

            def congrat():
                markup = types.InlineKeyboardMarkup()
                GoBack = types.InlineKeyboardButton(text="Назад в меню", callback_data="Menue")
                Write = types.InlineKeyboardButton(text="Повторить", callback_data="AddSynonim")
                markup.add(GoBack, Write)
                bot.send_message(message.chat.id, "Вернуться назад, или повторить", reply_markup=markup)

            nlp_result = NLP_CASE(SynWordText)

            def questionAuto2():
                send = bot.send_message(message.chat.id,
                                        f"Добавить к синониму <strong>{SynWordText}</strong> похожие слова?\n"
                                        f"Предпросмотр: <strong>{nlp_result}</strong>\n"
                                        f"Напишите боту <strong>'да'</strong> или <strong>'нет'</strong>.\n"
                                        "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.",
                                        parse_mode="html")
                bot.register_next_step_handler(send, answerAuto2)

            questionAuto2()



            # wordK = str(WordText) + "\n" # старое
            # print(wordK)


        # f.close()
        #
        # markup = types.InlineKeyboardMarkup()
        # GoBack = types.InlineKeyboardButton(text="Назад в меню", callback_data="Menue")
        # Write = types.InlineKeyboardButton(text="Повторить", callback_data="AddSynonim")
        # markup.add(GoBack, Write)
        # bot.send_message(message.chat.id, "Вернуться назад, или повторить", reply_markup=markup)

    SynToGlobal = message.text.lower()
    f = open('dict.txt', 'r', encoding='utf-8')
    f_lines = f.readlines()
    f.close()

    # стоп-слово
    if SynToGlobal == 'стоп':
        return bot.send_message(message.chat.id, 'Процесс остановлен.')

    check = False
    if SynToGlobal.find(' ') != -1:
        send = bot.send_message(message.chat.id, "Похоже, что вы ввели не одно слово, повторите пожалуйста\n"
                                                 "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
        check = True
        bot.register_next_step_handler(send, AddSynonimTo)

    # Есть ли ключевое слово в списке
    indexLINE = int()
    DoubleSyn = False
    for line in f_lines:
        line = line.replace('\n', '')
        words_in_line = line.split(' ')
        if words_in_line[0] == SynToGlobal:
            line = line + '\n'
            indexLINE = f_lines.index(line)
            DoubleSyn = True
            send = bot.send_message(message.chat.id, "Отлично, теперь введите синосим.\n"
                                                     "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
            bot.register_next_step_handler(send, AddSynonimWord)
            break

    # print(DoubleSyn)
    # print(check)
    if DoubleSyn == False and check == False:
        send = bot.send_message(message.chat.id, "Такое ключевое слово не найдено. \n"
                                                 "Введите ключевое слово, к которому хотите добавить синоним.\n"
                                                 "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.", parse_mode="html")
        bot.register_next_step_handler(send, AddSynonimTo)


# --------- ВЫГРУЗКА СЛОВАРЯ -------------

@bot.message_handler(commands=['dict'])
def UnloadDict(message):
    doc = open('dict.txt', 'rb')
    bot.send_document(message.chat.id, doc)

# --------- NLP PYMORPHY2/lemminflect ----
def NLP_CASE(a):
    if re.search('[a-zA-Z]', a):
        all_infl = getAllInflections(a)
        spisok = []
        for key, value in all_infl.items():
            for val in value:
                spisok.append(val)
        spisok = list(set(spisok))
        words = ' '.join(spisok)
        return words
    else:
        morph = pymorphy2.MorphAnalyzer(lang='ru')
        butyavka = morph.parse('%s' % a)[0]
        butyavka_lex = butyavka.lexeme

        words_lex = []
        # words_lex.append(a)
        for i in butyavka_lex:
            words_lex.append(i.word)
        words = ' '.join(words_lex) + '\n'
        return words

# --------- ПОИСК СТРОКИ В СЛОВАРЕ -------------
def FindingString(message):
    Fstring = message.text.lower()
    f = open('dict.txt', 'r', encoding='utf-8')
    f_lines = f.readlines()
    f.close()

    # стоп-слово
    if Fstring == 'стоп':
        return bot.send_message(message.chat.id, 'Процесс остановлен.')

    check = False
    if Fstring.find(' ') != -1:
        send = bot.send_message(message.chat.id, "Похоже, что вы ввели не одно слово, повторите пожалуйста.\n"
                                                 "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.",
                                                 parse_mode="html")
        check = True
        bot.register_next_step_handler(send, FindingString)

    # Есть ли ключевое слово в списке
    indexLINE = int()
    DoubleSyn = False
    for line in f_lines:
        line = line.replace('\n', '')
        words_in_line = line.split(' ')
        if words_in_line[0] == Fstring:
            line = line + '\n'
            indexLINE = f_lines.index(line)
            DoubleSyn = True
            break

    # print(DoubleSyn)
    # print(check)
    if DoubleSyn is False and check is False:
        send = bot.send_message(message.chat.id, "Такое ключевое слово не найдено. Попробуйте ещё раз. \n"
                                                 "Для отмены процесса напишите слово <strong><i>'стоп'</i></strong>.",
                                                 parse_mode="html")
        bot.register_next_step_handler(send, FindingString)
    if DoubleSyn is True and check is False:
        bot.send_message(message.chat.id, f"{f_lines[indexLINE]}")


# -------------- BACKUP DICT -------------------

async def backup_dict():
    doc = open('dict.txt', 'rb')
    bot.send_message(1883531134, 'Резервное копирование')
    bot.send_document(1883531134, doc)
    doc.close()


def execute_backup_dict():
    print('--бэкап--')
    asyncio.run(backup_dict())
    t = Timer(600.0, execute_backup_dict)  #3600.0 10ч
    t.start()
execute_backup_dict()


# -------------- СЛОВАРЬ (ПОИСК ПО СЛОВАРЮ) -----------------
def FindNews(mess):
    if mess.text.lower == 'стоп':
        return bot.send_message(mess.chat.id, 'Процесс остановлен.')  # ПОСТАВИЛА ВЫШЕ
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
            line = line.replace('\n', '')
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
                NewsNews = ParseNews
                ParseNews = ParseNews[:ParseNews.find("<a href=")]
                if ParseNews.lower().replace(':', ' ').replace('.', ' ').replace(',', ' ').replace('"', ' ') \
                        .replace('/', ' ').replace('\'', ' ').replace('ё', 'е').find(" " + word + " ") != -1:
                    TempParseResult.append(NewsNews)
        ParseResult = TempParseResult
        TempParseResult = []

    ParseResult = set(ParseResult)
    # print(ParseResult)

    # Вывод результата поиска в массиве+словаре
    if ParseResult == set():
        bot.send_message(message.chat.id, 'Извините, но новости по Вашему запросу не найдены. Попробуйте ещё раз.')
        markup = types.InlineKeyboardMarkup()
        GoBack = types.InlineKeyboardButton(text="Назад в меню", callback_data="Menue")
        Write = types.InlineKeyboardButton(text="Повторить", callback_data="FindByWord")
        markup.add(GoBack, Write)
        bot.send_message(message.chat.id, "Вернуться назад, или повторить", reply_markup=markup)
    else:
        for elem_r_set in ParseResult:
            # bot.send_message(message.chat.id, elem_r_set)
            bot.send_message(message.chat.id, elem_r_set, disable_web_page_preview=True, parse_mode='html')
        markup = types.InlineKeyboardMarkup()
        GoBack = types.InlineKeyboardButton(text="Назад в меню", callback_data="Menue")
        Write = types.InlineKeyboardButton(text="Повторить", callback_data="FindByWord")
        markup.add(GoBack, Write)
        bot.send_message(message.chat.id, "Вернуться назад, или повторить", reply_markup=markup)



# ----------------------- ЗАПУСК -------------------------

bot.infinity_polling()
