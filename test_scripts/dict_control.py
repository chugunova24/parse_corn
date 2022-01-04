import main

# добавление ключевого слова
def dict_new_word(message):
   f = open('../dict.txt', 'a', encoding='utf-8')
   word = 'wees'
   f.write('\n')
   f.write(word + ' ')
   f.close


# добавление синонимов к ключевому слову
def synonym(message):
   f = open('../dict.txt', 'a', encoding='utf-8')
   word = ['adssa', 'ааа', 'неееasdaеет']
   for elem in word:
      f.write(elem + ' ')
   f.close

# чтение последней строки, чтобы показать результат запроса
def print_last_line(message):
   f = open('../dict.txt', 'r', encoding='utf-8')
   last_line = f.readlines()[-1]
   f.close
   return last_line


# цикл чтения словаря, для поиска ключевого слова
def read_txt(message):
   message_lower_text = message.text.lower()

   try:
      n1 = main.zerno_ru()
      n2 = main.zol_ru()
      a = n1 + n2
      return a
   except Exception:
      print('ОШИБКА ПОИСКА')
   # print('ПОЛНЫЙ СПИСОК', a)


   def result_search_txt():
      key = '%s ' % message_lower_text

      f = open('../dict.txt', 'r', encoding='utf-8')
      f_lines = f.readlines()

      # поиск в файле строки с нужным набором слов (выход list)
      for line in f_lines:
         if key in line:
            return line

      # поиск в файле строки с нужным набором слов (выход str)
      for word in line:
         d = list(filter(word, a))
         print(d)

