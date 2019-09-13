#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
from pyquery import PyQuery as pq
from time import sleep
from tqdm import tqdm

links_scrolling = ['https://999.md/ru/category/real-estate/new-buildings/moldova/']


# In[ ]:


https://999.md/ru/category/real-estate/new-buildings/moldova/get_more?price_for=m2&price_from=0&price_to=999999&seed=0a6b9126-5425-44cf-bd1a-2c0338af63d9&page=1


# In[18]:


def parsepagesscrolling(links_scrolling, table_name):    
    page_number = 1
    errors_list = []
    for url_basic in links_scrolling:
        parse_list = []
        while True:
            url = url_basic + f'get_more?price_for=m2&price_from=0&price_to=999999&seed=0a6b9126-5425-44cf-bd1a-2c0338af63d9&page={page_number}'
            print(url)
            d = pq(url=url)
            if d("div.no-items__inner").text() == 'пусто':
                print(f'Страницы № {page_number} не существует')
                break
            else:
                for i in d("#list-items a").items():
                    link = 'https://999.md' + i.attr('href')
                    try:
                        conn = pq(url=link)

                        header = conn("body h1").text()
                        price_main = conn("#descriptions > div:nth-child(2) > div:nth-child(2) > div > div.col-md-8.col-sm-8.col-xs-12").text()
                        region = conn("#descriptions > div:nth-child(2) > div:nth-child(3) > div > div.col-md-8.col-sm-8.col-xs-12").text()
                        phone = conn("#descriptions div.item-view__options__item__phone").text().replace('\n', ' ')
                        nice_url = conn("[rel='alternate'][hreflang='ru']").attr('href')

                        parse_list.append([header,price_main,region,phone,nice_url])
                        parsed_df = pd.DataFrame(parse_list,columns = ['Заголовок','Цена','Регион','Контакты','Ссылка'])
                        parsed_df['Регион'] = parsed_df['Регион'].str.replace('Регион: ','')

                        parsed_df.to_excel(f'{table_name}.xlsx')
                        sleep(1)

                    except Exception as e: 
                        print('ERROR', e)
                        errors_list.append(link)
                        parsepagesscrolling.errors_list = errors_list
                        continue
                page_number += 1


# In[19]:


parsepagesscrolling(links_scrolling,'new-buildings')


# # Задача
# * Получить ссылки (для дальнейшего парсинга, не для таблицы):<br>
# `for i in d("#list-items a").items():
#     link = 'https://999.md' + i.attr('href')`
# <br>
# * Получить заголовок:<br>
# `conn("body h1").text()`
# <br>
# * Получить цену:<br>
# `conn("#descriptions > div:nth-child(2) > div:nth-child(2) > div > div.col-md-8.col-sm-8.col-xs-12").text()`
# <br>
# * Получить адрес ("регион"):<br>
# `conn("#descriptions > div:nth-child(2) > div:nth-child(3) > div > div.col-md-8.col-sm-8.col-xs-12").text()`<br>
# * Получить контакты:<br>
# `conn("#descriptions div.item-view__options__item__phone").text().replace('\n', ' ')`
# * Красивая ссылка для таблицы:<br>
# `conn("[rel='alternate'][hreflang='ru']").attr('href')`
# <br>

# In[ ]:




