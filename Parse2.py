#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pyquery import PyQuery as pq
from time import sleep
from tqdm import tqdm


# In[2]:


links_pages_final0 = [
         {'url':'https://999.md/ru/list/real-estate/miscellaneous',
          'max_pages':4,
         'name':'miscellaneous'},
         {'url':'https://999.md/ru/list/real-estate/services',
          'max_pages':5,
         'name':'services'}
]

links_pages_final2 = [
         {'url':'https://999.md/ru/list/real-estate/house-and-garden',
          'max_pages':184,
         'name':'house-and-garden'},
         {'url':'https://999.md/ru/list/real-estate/land',
          'max_pages':114,
         'name':'land'}
]

links_pages_final1 = [
         {'url':'https://999.md/ru/list/real-estate/garages-and-parking',
          'max_pages':22,
         'name':'garages-and-parking'}
]

links_pages_final4 = [
    {'url':'https://999.md/ru/list/real-estate/commercial-real-estate',
     'max_pages':109,
     'name':'commercial-real-estate'}
    
]


# In[20]:


links_pages_final31 = [
         {'url':'https://999.md/ru/list/real-estate/apartments-and-rooms',
          'start_page':1,
          'max_pages':100,
         'name':'apartments-and-rooms1'}
]

links_pages_final32 = [
         {'url':'https://999.md/ru/list/real-estate/apartments-and-rooms',
          'start_page':101,
          'max_pages':200,
         'name':'apartments-and-rooms2'}
]

links_pages_final33 = [
         {'url':'https://999.md/ru/list/real-estate/apartments-and-rooms',
          'start_page':201,
          'max_pages':300,
         'name':'apartments-and-rooms3'}
]

links_pages_final34 = [
         {'url':'https://999.md/ru/list/real-estate/apartments-and-rooms',
          'start_page':301,
          'max_pages':400,
         'name':'apartments-and-rooms4'}
]

links_pages_final35 = [
         {'url':'https://999.md/ru/list/real-estate/apartments-and-rooms',
          'start_page':401,
          'max_pages':500,
         'name':'apartments-and-rooms5'}
]

links_pages_final36 = [
         {'url':'https://999.md/ru/list/real-estate/apartments-and-rooms',
          'start_page':501,
          'max_pages':587,
         'name':'apartments-and-rooms6'}
]


# In[4]:


links_pages_test1 = [
         {'url':'https://999.md/ru/list/real-estate/apartments-and-rooms',
          'max_pages':2,
         'name':'apartments-and-rooms'}
]

links_pages_test2 = [
         {'url':'https://999.md/ru/list/real-estate/apartments-and-rooms',
          'max_pages':2,
         'name':'apartments-and-rooms'},
         {'url':'https://999.md/ru/list/real-estate/house-and-garden',
          'max_pages':2,
         'name':'house-and-garden'}
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

# # Проверка

# ## Проверка финальных страниц

# In[217]:


url = "https://999.md/ru/27740665"
conn = pq(url=url)
header = conn("header.adPage__header h1").text()
price_main = conn("[class=' tooltip adPage__content__price-feature__prices__price is-main ']").text()
region = conn("dl[class='adPage__content__region grid_18']").text().replace('\n', ' ')
phone = conn("strong").text()
nice_url = conn("[property='og:url']").attr('content')
print(header,price_main,region,phone,nice_url, sep='\n')


# ### проерка пройдена

# ## Проверка с главных страниц

# In[271]:


url = "https://999.md/ru/list/real-estate/apartments-and-rooms"
conn = pq(url=url)


# In[274]:


dfs_dict = {}
        
q = 0

parse_list = []

for i in conn("#js-ads-container div.ads-list-photo-item-title a").items():
    if q < 2:
        
        link = 'https://999.md' + i.attr('href')
        conn2 = pq(url=link)

        header = conn2("header.adPage__header h1").text()
        price_main = conn2("[class=' tooltip adPage__content__price-feature__prices__price is-main ']").text()
        region = conn2("dl[class='adPage__content__region grid_18']").text().replace('\n', ' ')
        phone = conn2("strong").text()
        nice_url = conn2("[property='og:url']").attr('content')
        
        parse_list.append([header,price_main,region,phone,nice_url]) 
        
        q += 1    
    
    else:
        break
    
parsed_df = pd.DataFrame(parse_list,columns = ['Заголовок','Цена','Регион','Контакты','Ссылка'])


# In[275]:


parsed_df


# ### проверка пройдена

# ## Полная проверка массовая одна страница

# In[278]:


dfs_dict = {}

for item in links_pages_test1:
    
    parse_list = []
    
    table_name = item['name']
    url_basic = item['url']
    max_pages = item['max_pages']
    
    for page in range(1,max_pages+1):
        url = url_basic + f'?page={page}'
        d = pq(url=url)
        for i in d("#js-ads-container div.ads-list-photo-item-title a").items():
            
            link = 'https://999.md' + i.attr('href')
            conn = pq(url=link)
            
            header = conn("header.adPage__header h1").text()
            price_main = conn("[class=' tooltip adPage__content__price-feature__prices__price is-main ']").text()
            region = conn("dl[class='adPage__content__region grid_18']").text().replace('\n', ' ')
            phone = conn("strong").text()
            nice_url = conn("[property='og:url']").attr('content')
            
            parse_list.append([header,price_main,region,phone,nice_url])
            
    parsed_df = pd.DataFrame(parse_list,columns = ['Заголовок','Цена','Регион','Контакты','Ссылка'])
    dfs_dict[table_name] = parsed_df


# In[280]:


dfs_dict['apartments-and-rooms']


# ### проверка пройдена

# ## Полная проверка массовая несколько страниц

# In[281]:


dfs_dict = {}

for item in links_pages_final:
    
    parse_list = []
    
    table_name = item['name']
    url_basic = item['url']
    max_pages = item['max_pages']
    
    for page in range(1,max_pages+1):
        url = url_basic + f'?page={page}'
        d = pq(url=url)
        for i in d("#js-ads-container div.ads-list-photo-item-title a").items():
            link = 'https://999.md' + i.attr('href')
            conn = pq(url=link)
            
            
            header = conn("header.adPage__header h1").text()
            price_main = conn("[class=' tooltip adPage__content__price-feature__prices__price is-main ']").text()
            region = conn("dl[class='adPage__content__region grid_18']").text().replace('\n', ' ')
            phone = conn("strong").text()
            nice_url = conn("[property='og:url']").attr('content')
            
            parse_list.append([header,price_main,region,phone,nice_url])
            
    parsed_df = pd.DataFrame(parse_list,columns = ['Заголовок','Цена','Регион','Контакты','Ссылка'])
    dfs_dict[table_name] = parsed_df


# In[285]:


dfs_dict['apartments-and-rooms']


# In[286]:


dfs_dict['house-and-garden']


# ### проверка пройдена

# # Страницы без скроллинга

# In[ ]:


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


# In[16]:


def parsepagessplit(links_pages_final):
    dfs_dict = {}
    errors_list = []

    for item in tqdm(links_pages_final):
        parse_list = []

        table_name = item['name']
        url_basic = item['url']
        start_page = item['start_page']
        max_pages = item['max_pages']

        for page in tqdm(range(start_page,max_pages+1)):
            
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
                    
                except Exception as e: 
                    print('ERROR', e)
                    errors_list.append(link)
                    parsepagessplit.errors_list = errors_list
                    sleep(1)
                    continue
                
        dfs_dict[table_name] = parsed_df
                    
        parsepagessplit.dfsDict = dfs_dict


# In[17]:


parsepagessplit(links_pages_final31)


# In[21]:


parsepagessplit(links_pages_final32)


# In[22]:


parsepagessplit(links_pages_final33)


# In[23]:


parsepagessplit(links_pages_final34)


# In[24]:


parsepagessplit(links_pages_final35)


# In[25]:


parsepagessplit(links_pages_final36)


# In[26]:


df1 = pd.read_excel('apartments-and-rooms1.xlsx')
df2 = pd.read_excel('apartments-and-rooms2.xlsx')
df3 = pd.read_excel('apartments-and-rooms3.xlsx')
df4 = pd.read_excel('apartments-and-rooms4.xlsx')
df5 = pd.read_excel('apartments-and-rooms5.xlsx')
df6 = pd.read_excel('apartments-and-rooms6.xlsx')


# In[33]:


df_final = pd.concat([df1,df2,df3,df4,df5,df6])


# In[43]:


len(df1)+len(df2)+len(df3)+len(df4)+len(df5)+len(df6)


# In[44]:


df_final.reset_index()


# In[47]:


len(df_final.drop_duplicates())


# In[46]:


df_final.to_excel('apartments-and-rooms-final.xlsx')


# In[48]:


df_final.drop_duplicates().to_excel('apartments-and-rooms-final-no-duplicates.xlsx')

