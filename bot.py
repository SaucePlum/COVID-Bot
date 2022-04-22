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
from qqbot.model.message import MessageMarkdown

from command_register import command

config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yml"))
T_TOKEN = qqbot.Token(config["bot"]["appid"], config["bot"]["token"])


async def _invalid_func(event: str, message: qqbot.Message):
    """
    当参数不符合要求时的处理函数
    """
    await _send_message("请在指令后带上城市名称，例如\r\n/油价 深圳", event, message)
    return True


async def _send_message(content: str, event: str, message: qqbot.Message, is_markdown: bool = False):
    """
    机器人发送消息
    """
    msg_api = qqbot.AsyncMessageAPI(T_TOKEN, False)
    dms_api = qqbot.AsyncDmsAPI(T_TOKEN, False)

    send = qqbot.MessageSendRequest(content=content, msg_id=message.id)
    if is_markdown and event != "DIRECT_MESSAGE_CREATE":
        markdown = MessageMarkdown()
        markdown.content = content
        send = qqbot.MessageSendRequest(content="", markdown=markdown, msg_id=message.id)

    if event == "DIRECT_MESSAGE_CREATE":
        await dms_api.post_direct_message(message.guild_id, send)
    else:
        await msg_api.post_message(message.channel_id, send)


@command("/菜单")
async def ask_menu(city_name: str, event: str, message: qqbot.Message):
    ret = get_menu()
    await _send_message(ret, event, message, True)
    return True


@command("/油价", check_param=True, invalid_func=_invalid_func)
async def ask_price(city_name: str, event: str, message: qqbot.Message):
    ret = get_prices_str(await get_data(city_name), 0)
    await _send_message(ret, event, message)
    return True


@command("/0号油价", check_param=True, invalid_func=_invalid_func)
async def ask_price0(city_name: str, event: str, message: qqbot.Message):
    ret = get_prices_str(await get_data(city_name), 1)
    await _send_message(ret, event, message)
    return True


@command("/92油价", check_param=True, invalid_func=_invalid_func)
async def ask_price92(city_name: str, event: str, message: qqbot.Message):
    ret = get_prices_str(await get_data(city_name), 2)
    await _send_message(ret, event, message)
    return True


@command("/95油价", check_param=True, invalid_func=_invalid_func)
async def ask_price95(city_name: str, event: str, message: qqbot.Message):
    ret = get_prices_str(await get_data(city_name), 3)
    await _send_message(ret, event, message)
    return True


@command("/加油优惠", check_param=True, invalid_func=_invalid_func)
async def ask_discount(city_name: str, event: str, message: qqbot.Message):
    ret = get_discount_str(await get_data(city_name))
    await _send_message(ret, event, message, True)
    return True


async def _message_handler(event: str, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """

    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)

    tasks = [
        ask_menu,  # /菜单
        ask_price,  # /油价
        ask_price0,  # /0号油价
        ask_price92,  # /92油价
        ask_price95,  # /95油价
        ask_discount,  # /加油优惠
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
    qqbot.async_listen_events(T_TOKEN, False, qqbot_handler, qqbot_direct_handler)


if __name__ == "__main__":
    run()