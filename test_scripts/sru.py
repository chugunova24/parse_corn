a = ['aaaa', 'bbbbb', 'cccccc', 'dddddd', 'fffff', 'gggggg', 'eeeeee']

with open('aboba.txt', 'w') as file:
    file.truncate()
    for i in a:
        file.write(i + '\n')
    file.close()
