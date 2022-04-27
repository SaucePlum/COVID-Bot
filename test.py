#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test.py: 

Author: NianGui
Time  : 2022/4/26 0026 21:54
"""


import json
import requests

url = 'https://file1.dxycdn.com/2020/0223/046/3398299755968039975-135.json'


content = requests.get(url).json()['data']

print(content)