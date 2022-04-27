#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test.py: 

Author: NianGui
Time  : 2022/4/26 0026 21:54
"""

import requests
from bs4 import BeautifulSoup
url = 'https://heihaoma.com/i-fangyi'
res = requests.get(url).text
content = BeautifulSoup(res, 'html.parser')
data_first = content.find('div', attrs={'id' : 'container'})
data_two = data_first.find_all('li')

for city_data in data_two:
    city_name = city_data.find('div',attrs={'class' : 'contact-tit'}).text
    city_phone = city_data.find('div',attrs={'class' : 'contact-phone'}).text




# city_list = etree_html.xpath('//*[@id="container"]/li/text()')
#
# for city in city_list:
#     print(city)