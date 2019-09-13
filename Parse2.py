#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pyquery import PyQuery as pq
from time import sleep
from tqdm import tqdm

links_pages_final = [
         {'url':'https://999.md/ru/list/real-estate/miscellaneous',
          'max_pages':4,
         'name':'miscellaneous'},
         {'url':'https://999.md/ru/list/real-estate/services',
          'max_pages':5,
         'name':'services'}
]


# # Задача
# * Получить ссылки (для дальнейшего парсинга, не для таблицы):<br>
# `for i in d("#list-items a").items():
#     link = 'https://999.md' + i.attr('href')`
# <br>
# * Получить заголовок:<br>
# `conn("header.adPage__header h1").text()`
# <br>
# * Получить цену:<br>
# `conn("[class=' tooltip adPage__content__price-feature__prices__price is-main ']").text()`
# <br>
# * Получить адрес ("регион"):<br>
# `conn("dl[class='adPage__content__region grid_18']").text().replace('\n', ' ')`<br>
# * Получить контакты:<br>
# `conn("strong").text()`
# * Красивая ссылка для таблицы:<br>
# `conn("[property='og:url']").attr('content')`
# <br>

def parsepages(links_pages_final):
    dfs_dict = {}
    parsepages.errors_list = []

    for item in tqdm(links_pages_final):
        parse_list = []

        table_name = item['name']
        url_basic = item['url']
        max_pages = item['max_pages']

        for page in tqdm(range(1,max_pages+1)):
            print(f'parsing page no. {page}')
            
            url = url_basic + f'?page={page}'
            d = pq(url=url)
            for i in d("#js-ads-container div.ads-list-photo-item-title a").items():
                link = 'https://999.md' + i.attr('href')
                try:
                    conn = pq(url=link)

                    header = conn("header.adPage__header h1").text()
                    price_main = conn("[class=' tooltip adPage__content__price-feature__prices__price is-main ']").text()
                    region = conn("dl[class='adPage__content__region grid_18']").text().replace('\n', ' ')
                    phone = conn("strong").text()
                    nice_url = conn("[property='og:url']").attr('content')

                    parse_list.append([header,price_main,region,phone,nice_url])
                                        
                    parsed_df = pd.DataFrame(parse_list,columns = ['Заголовок','Цена','Регион','Контакты','Ссылка'])
                    parsed_df['Регион'] = parsed_df['Регион'].str.replace('Регион: ','')
                                        
                    parsed_df.to_excel(f'{table_name}.xlsx')
                    sleep(1)
                    
                except:
                    print('error')
                    parsepages.errors_list.append(link)
                    sleep(1)
                    continue
                
        dfs_dict[table_name] = parsed_df
                    
        parsepages.dfsDict = dfs_dict
