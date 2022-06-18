# -*- coding: utf-8 -*-
import random

import botpy
from botpy import BotAPI
from botpy.message import Message

from command_register import Commands
from util import get_menu, get_covid_data, get_grade_data, get_news_data, get_policy, get_policys, get_covid_phone, \
    science, science_images


async def covid(message: Message):
    await message.reply(
        content="请在指令后带上城市名称\n\n例如：@疫情助手 /疫情 深圳"
    )
    return True

async def grade(message: Message):
    await message.reply(
        content="请在指令后带上城市名称\n\n例如：@疫情助手 /风险地区 深圳"
    )
    return True

async def covid_phone(message: Message):
    await message.reply(
        content="请在指令后带上城市名称\n\n例如：@疫情助手 /防疫热线 深圳"
    )
    return True

async def policy(message: Message):
    await message.reply(
        content="请在指令后带上城市名称\n\n当地政策：@疫情助手 /出行政策 深圳\n两地政策：@疫情助手 /出行政策 深圳-广州"
    )
    return True

@Commands("/菜单")
async def ask_menu(api: BotAPI, message: Message, params=None):
    await message.reply(content=get_menu())
    return True

@Commands("/疫情资讯")
async def ask_news(api: BotAPI, message: Message, params=None):
    ret = await get_news_data()
    await message.reply(content=ret)
    return True

@Commands("/出行政策")
async def ask_policy(api: BotAPI, message: Message, params=None):
    if params:
        await policy(message)
        return True
    if '-' in params:
        from_city = params.split('-')[0]
        to_city = params.split('-')[1]
        ret = await get_policys(from_city, to_city)
    else:
        ret = await get_policy(params)
    if ret == '':
        await message.reply(content=get_menu())
        return True
    await message.reply(content=ret)
    return True

@Commands("/疫情科普")
async def ask_science(api: BotAPI, message: Message, params=None):
    await api.post_message(
        channel_id=message.id,
        content=random.choice(science),
        image=random.choice(science_images),
        msg_id=message.id,
    )
    return True

@Commands("/疫情")
async def ask_covid(api: BotAPI, message: Message, params=None):
    params = "中国" if params is None else params
    ret = await get_covid_data(params)
    if ret == '':
        await message.reply(content=get_menu())
        return True
    await message.reply(content=ret)
    return True

@Commands("/防疫热线")
async def ask_covid_phone(api: BotAPI, message: Message, params=None):
    if params:
        await covid_phone(message)
        return True
    ret = await get_covid_phone(params)
    if ret == '':
        await message.reply(content="未找到该地防疫热线电话")
        return True
    await message.reply(content=ret)
    return True

@Commands("/风险地区")
async def ask_grade(api: BotAPI, message: Message, params=None):
    if params:
        await grade(message)
        return True
    ret = await get_grade_data(params)
    await message.reply(content=ret)
    return True


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        tasks = [
            ask_menu,  # /菜单
            ask_science,  # /疫情科普
            ask_news,  # /疫情资讯
            ask_policy,  # /出行政策
            ask_covid,  # /疫情
            ask_covid_phone,  # /防疫热线
            ask_grade,  # /风险地区
        ]
        for handler in tasks:
            if await handler(api=self.api, message=message):
                return

if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid="appid", token="token")
