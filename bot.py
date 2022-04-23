#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bot.py.py: 疫情助手主程序

Author: NianGui
Time  : 2022/4/23 0:29
"""
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil

from command_register import command
from util import get_menu, get_covid_data, get_grade_data

config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yml"))
T_TOKEN = qqbot.Token(config["bot"]["appid"], config["bot"]["token"])


async def _invalid_func(event: str, message: qqbot.Message):
    """
    当参数不符合要求时的处理函数
    """
    await _send_message("请在指令后带上城市名称\n例如\r\n/疫情 深圳\r\n/风险地区 深圳", event, message)
    return True


async def _send_message(
    content: str, event: str, message: qqbot.Message, is_markdown: bool = False
):
    """
    机器人发送消息
    """
    msg_api = qqbot.AsyncMessageAPI(T_TOKEN, False)
    dms_api = qqbot.AsyncDmsAPI(T_TOKEN, False)

    send = qqbot.MessageSendRequest(content=content, msg_id=message.id)
    if event == "DIRECT_MESSAGE_CREATE":
        await dms_api.post_direct_message(message.guild_id, send)
    else:
        await msg_api.post_message(message.channel_id, send)


@command("/菜单")
async def ask_menu(city_name: str, event: str, message: qqbot.Message):
    ret = get_menu()
    await _send_message(ret, event, message, True)
    return True


@command("/疫情", check_param=True, invalid_func=_invalid_func)
async def ask_covid(city_name: str, event: str, message: qqbot.Message):
    city_name = "中国" if city_name is None else city_name
    ret = get_covid_data(city_name)
    await _send_message(ret, event, message)
    return True


@command("/风险地区", check_param=True, invalid_func=_invalid_func)
async def ask_grade(city_name: str, event: str, message: qqbot.Message):
    ret = get_grade_data(city_name)
    await _send_message(ret, event, message)
    return True


async def _message_handler(event: str, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    qqbot.logger.info("收到消息: %s" % message.content)

    tasks = [
        ask_menu,  # /菜单
        ask_covid,  # /疫情
        ask_grade,  # /风险地区
    ]
    for task in tasks:
        if await task("", event, message):
            return
    await _send_message("抱歉，没明白你的意思呢。" + get_menu(), event, message)


def run():
    """
    启动机器人
    """
    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    # 私信消息
    qqbot_direct_handler = qqbot.Handler(
        qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(T_TOKEN, True, qqbot_handler, qqbot_direct_handler)


if __name__ == "__main__":
    run()
