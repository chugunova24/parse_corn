parse_result = ['Под лежачий щебень вагон не идет <a href="https://www.kommersant.ru/doc/5182072">kommersant.ru</a>',
                'Пандемия брендировала не всех <a href="https://www.kommersant.ru/doc/5182157">kommersant.ru</a>',
                'Общественная палата сообщила о недовольстве детей школьным питанием <a href="https://www.kommersant.ru/doc/5182194">kommersant.ru</a>',
                'В молоко добавляют инноваций <a href="https://www.kommersant.ru/doc/5182070">kommersant.ru</a>',
                'Отельеры перестроили тарифы <a href="https://www.kommersant.ru/doc/5182026">kommersant.ru</a>',
                'От COVID-19 подбирают средство <a href="https://www.kommersant.ru/doc/5181979">kommersant.ru</a>',
                'Кашам — крышка <a href="https://www.kommersant.ru/doc/5181973">kommersant.ru</a>',
                'Путин попросил правительство и ЦБ прийти к единому мнению по криптовалютам <a href="https://www.kommersant.ru/doc/5182748">kommersant.ru</a>',
                'Госдума приняла закон о штрафах за переводы нелегальным онлайн-казино <a href="https://www.kommersant.ru/doc/5182612">kommersant.ru</a>',
                'Биржевые цены на топливо обновили рекорды <a href="https://www.kommersant.ru/doc/5182583">kommersant.ru</a>',
                'В Казани предложили создать пилотную зону крипторынка <a href="https://www.kommersant.ru/doc/5182477">kommersant.ru</a>',
                'Лавров: США делают все, чтобы подорвать доверие к доллару <a href="https://www.kommersant.ru/doc/5182493">kommersant.ru</a>']

for i in parse_result:
    print(i[:i.find("<a href=")])