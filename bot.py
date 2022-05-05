#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bot.py.py: 疫情助手主程序

Author: NianGui
Time  : 2022/4/23 0:29
"""
import os.path
import random

import qqbot
from qqbot.core.util.yaml_util import YamlUtil

from command_register import command
from util import get_menu, get_covid_data, get_grade_data, get_news_data, get_policy, get_policys, get_covid_phone

config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yml"))
T_TOKEN = qqbot.Token(config["bot"]["appid"], config["bot"]["token"])


async def _invalid_func(event: str, message: qqbot.Message):
    """
    当参数不符合要求时的处理函数
    """
    await _send_message("请在指令后带上城市名称\n\n" + get_menu(), event, message)
    return True


async def _send_message(
    content: str, event: str, message: qqbot.Message, image: str = None
):
    """
    机器人发送消息
    """
    msg_api = qqbot.AsyncMessageAPI(T_TOKEN, False)
    dms_api = qqbot.AsyncDmsAPI(T_TOKEN, False)

    send = qqbot.MessageSendRequest(content=content, msg_id=message.id, image=image)
    if event == "DIRECT_MESSAGE_CREATE":
        await dms_api.post_direct_message(message.guild_id, send)
    else:
        await msg_api.post_message(message.channel_id, send)


@command("/菜单")
async def ask_menu(city_name: str, event: str, message: qqbot.Message):
    await _send_message(get_menu(), event, message)
    return True


@command("/疫情资讯")
async def ask_news(city_name: str, event: str, message: qqbot.Message):
    ret = await get_news_data()
    await _send_message(ret, event, message)
    return True


@command("/出行政策", check_param=True, invalid_func=_invalid_func)
async def ask_policy(city_name: str, event: str, message: qqbot.Message):
    if '-' in city_name:
        from_city = city_name.split('-')[0]
        to_city = city_name.split('-')[1]
        ret = await get_policys(from_city, to_city)
    else:
        ret = await get_policy(city_name)
    if ret == '':
        await _send_message(get_menu(), event, message)
        return True
    await _send_message(ret, event, message)
    return True


@command("/疫情科普")
async def ask_science(city_name: str, event: str, message: qqbot.Message):
    science = [
        '包里备好消毒湿巾、酒精喷雾、酒精棉片、免洗洗手液、一次性手套。别嫌东西多包重，相信我，你大概率会用得上。',
        '出门前戴好口罩，进公司后也别脱，它将是你一天的保护色。最好能包里准备了2—3个备用（如果你买得到的话），到公司后更换口罩，尽量建议到空旷无人地区。',
        '饮食专家建议：适量饮水，每天不少于1500ml。',
        '在平静状态下测得体温为37.3度即可判断为发热。',
        '感染新冠肺炎的患者，大约会在1周后出现呼吸困难、严重者会出现凝血功能障碍、急性呼吸窘迫综合征等严重症状。',
        '通常来讲，1岁以下的孩子不适合戴口罩。',
        '新冠病毒从发病到入院的中位时间是11天。',
        '新型冠状病毒肺炎确诊需要：流行病学史+临床表现+新型冠状病毒核酸检测。',
        '新型冠状病毒肺炎感染的报告时间为2小时。',
        '冠状病毒感染后免疫系统对肺细胞的攻击引发肺炎，此时可以通过适度使用免疫抑制剂对病人进行治疗，避免肺部严重受损。',
        '家庭置备体温计、口罩、家用消毒用品等物品。未接触过疑似或确诊患者且外观完好、无异味或脏污的口罩，回家后可放置于居室通风干燥处,以备下次使用。需要丢弃的口罩，按照生活垃圾分类的要求处理。',
        '随时保持手卫生，从公共场所返回、咳嗽手捂之后、饭前便后，用洗手液或香皂流水洗手，或者使用免洗洗手液。不确定手是否清洁时，避免用手接触口鼻眼。打喷嚏或咳嗽时，用手肘衣服遮住口鼻。',
        '保持良好的生活习惯。居室整洁，勤开窗，经常通风，定时消毒。平衡膳食，均衡营养，适度运动，充分休息，不随地吐痰，口鼻分泌物用纸巾包好，弃置于有盖的垃圾箱内。',
        '尽量减少外出活动。减少走亲访友和聚餐，尽量在家休息。减少到人员密集的公共场所活动，尤其是相对封闭、空气流动差的场所，例如公共浴池、温泉、影院、网吧、KTV、商场、车站、机场、码头和展览馆等。',
        '根据具体条件适当参加户外锻炼，提高免疫力与生活质量。在户外活动过程中应避免与同伴以外的人近距离接触，注意个人卫生，不随地吐痰，打喷嚏或咳嗽时用肘部或纸巾遮住。',
        '前往公众场所时应遵守相关部门规定，使用健康码等手段确认行动轨迹、健康状况等信息，获得许可后方可进入。',
        '若出现发热、咳嗽、咽痛、胸闷、呼吸困难、乏力、恶心呕吐、腹泻、结膜炎、肌肉酸痛等可疑症状，应根据病情，及时到医疗机构就诊。',
        '回家之后，请把外套挂在在通风处，不推荐喷酒精消毒，一是因为容易破坏衣物；二是冬天起静电火花遇上酒精很危险。',
        '摘口罩时，记住4个“不要”：\n不要触碰口罩的外表面\n不要触碰口罩的内表面\n不要触碰别人使用过的口罩，避免交叉感染\n不要直接放在包里、兜里等处，容易造成持续感染风险，可以由内向外反向折叠后，用自封袋包装\n摘口罩的时候，尽量避免污染区（外面），主要摘下耳挂。',
        '触摸被污染的物体表面，然后用脏手触碰嘴巴、鼻子或眼睛，这些均为新型冠状病毒可能的传播途径。',
        '通过咳嗽或打喷嚏在空气传播，飞沫随着空气在飘荡，如果没有防护，非常容易中招。',
        '什么是密切接触者？\n\n病例的密切接触者，即与病例发病后有如下接触情形之一，但未采取有效防护者：\n·与病例共同居住、学习、工作，或其他有密切接触的人员，如与病例近距离工作或共用同一教室或与病例在同一所房屋中生活；\n·诊疗、护理、探视病例的医护人员、家属或其他与病例有类似近距离接触的人员，如直接治疗及护理病例、到病例所在的密闭环境中探视病人或停留，病例同病室的其他患者及其陪护人员；\n·与病例乘坐同一交通工具并有近距离接触人员，包括在交通工具上照料护理过病人的人员；该病人的同行人员（家人、同事、朋友等）；经调查评估后发现有可能近距离接触病人的其他乘客和乘务人员；',
        '密切接触者应该怎么做？\n\n密切接触者应进行隔离医学观察。\n居家或集中隔离医学观察，观察期限为自最后一次与病例发生无有效防护的接触或可疑暴露后14天。\n居家医学观察时应独立居住，尽可能减少与其他人员的接触。尽量不要外出。如果必须外出，需经医学观察管理人员批准，并要佩戴一次性外科口罩，避免去人群密集场所。\n·医学观察期间，应配合指定的管理人员每天早、晚各进行一次体温测量，并如实告知健康状况。\n医学观察期间出现发热、咳嗽、气促等急性呼吸道感染症状者，应立即到定点医疗机构诊治。\n医学观察期满时，如未出现上述症状，则解除医学观察。',
        '为什么要对密切接触者医学观察14天？\n\n目前对密切接触者采取较为严格的医学观察等预防性公共卫生措施十分必要，这是一种对公众健康安全负责任的态度，也是国际社会通行的做法。参考其他冠状病毒所致疾病潜伏期、此次新型冠状病毒病例相关信息及当前防控实际，将密切接触者医学观察期定为14天，并对密切接触者进行医学观察。',
        '如果接到疾控部门通知，你是－个密切接触者，该怎么办？\n\n不用恐慌，按照要求进行居家或集中隔离医学观察。如果是在家中进行医学观察，请不要上班，不要随便外出，做好自我身体状况观察，定期接受社区医生随访，如果出现发热、咳嗽等异常临床表现，及时向当地疾病预防控制机构报告，在其指导下到指定医疗机构进行排查、诊治等。',
    ]
    science_images = [
        'http://images.china.cn/site1000/2020-02/05/43fb2c2d-07f3-4ed9-a1ab-69e8ad9aa5e3.jpg',
        'http://images.china.cn/site1000/2020-02/05/bda956f4-0e18-4b19-9299-2b9ffb7927c5.jpg',
        'http://images.china.cn/site1000/2020-02/05/11167389-3724-4aa4-ae49-ff97380c00ed.jpg',
        'http://images.china.cn/site1000/2020-02/05/11167389-3724-4aa4-ae49-ff97380c00ed.jpg',
        'http://images.china.cn/site1000/2020-02/05/7d058780-c2f1-476a-bc80-f5bae96bea1f.jpg',
        'http://images.china.cn/site1000/2020-02/05/0a4ba046-ebe1-4c54-b377-b0e27281db50.png',
        'http://images.china.cn/site1000/2020-02/05/35cbab10-524e-4f52-b7b5-4ebcd9c3180b.png',
        'http://images.china.cn/site1000/2020-02/05/69ec7ce4-8875-4215-8545-3b83b6cf0e10.png',
        'http://images.china.cn/site1000/2020-02/05/0b5fe2e7-03fd-4201-b1a7-deb2a794e589.jpg',
        'http://images.china.cn/site1000/2020-02/05/0f08ee36-ff04-4c2d-8c0c-fa5da494595d.jpg',
        'http://images.china.cn/site1000/2020-02/05/4d643e39-ac5d-4c46-bbe1-1ed43fa5464a.jpg',
        'http://images.china.cn/site1000/2020-02/05/4d643e39-ac5d-4c46-bbe1-1ed43fa5464a.jpg',
        'http://images.china.cn/site1000/2020-02/05/eb69ed80-9f28-4998-a755-a8d65e0473d0.png',
        'http://images.china.cn/site1000/2020-02/05/27f0ebc5-2452-4374-ad62-3829ead85a68.png',
        'http://images.china.cn/site1000/2020-02/05/34e837f9-4707-4caf-8d22-708554204b65.png',
        'http://images.china.cn/site1000/2020-02/05/ef001555-38f6-4ef3-ae6a-2421587f903b.png',
        'http://images.china.cn/site1000/2020-02/05/25ca3965-c907-4822-9835-c2b639877cf9.jpg',
        'http://images.china.cn/site1000/2020-02/05/1724708c-8fa8-4494-82eb-2ee090954e83.jpg',
        'http://images.china.cn/site1000/2020-02/05/9e03d23d-0f7a-4f3b-872d-d8bf816af70f.jpg',
        'http://images.china.cn/site1000/2020-02/05/bc807de8-9a61-4baf-a0b1-1ea5915d7d2f.jpg'
    ]
    await _send_message(random.choice(science), event, message, random.choice(science_images))

    return True


@command("/疫情", check_param=True, invalid_func=_invalid_func)
async def ask_covid(city_name: str, event: str, message: qqbot.Message):
    city_name = "中国" if city_name is None else city_name
    ret = await get_covid_data(city_name)
    if ret == '':
        await _send_message(get_menu(), event, message)
        return True
    await _send_message(ret, event, message)
    return True


@command("/防疫热线", check_param=True, invalid_func=_invalid_func)
async def ask_covid_phone(city_name: str, event: str, message: qqbot.Message):
    ret = await get_covid_phone(city_name)
    if ret == '':
        await _send_message('未找到该地防疫热线电话', event, message)
        return True
    await _send_message(ret, event, message)
    return True


@command("/风险地区", check_param=True, invalid_func=_invalid_func)
async def ask_grade(city_name: str, event: str, message: qqbot.Message):
    ret = await get_grade_data(city_name)
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
        ask_science, # /疫情科普
        ask_news, # /疫情资讯
        ask_policy, # /出行政策
        ask_covid,  # /疫情
        ask_covid_phone, # /防疫热线
        ask_grade,  # /风险地区
    ]
    for task in tasks:
        if await task("", event, message):
            return
    await _send_message("抱歉，没明白你的意思呢。\n" + get_menu(), event, message)


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
