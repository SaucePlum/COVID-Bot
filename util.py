#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
util.py: 疫情助手核心

Author: NianGui
Time  : 2022/4/23 1:01
"""
import json
import os
import time

import qqbot
import requests
from bs4 import BeautifulSoup

# 疫情数据API > 腾讯
covid_url = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf"
# 风险地区API > 腾讯
grade_url = "https://wechat.wecity.qq.com/api/PneumoniaTravelNoAuth/queryAllRiskLevel"
# 疫情资讯API > 百度
news_url = "https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&dspName=iphone&from_sf=1&dsp=iphone&resource_id=28565&alr=1&query=国内新型肺炎最新动态&cb="

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


def get_menu():
    return """/疫情 城市
    查询指定城市当天疫情数据
    示例：/疫情 深圳
/风险地区 城市
    查询国内风险地区
    示例：/风险地区 深圳
/出行政策 出发地-到达地
    查询国内出行政策
    示例：/出行政策 深圳-广州
    可单个地区查询
    示例：/出行政策 深圳
/疫情资讯
    查询疫情最新新闻动态
    示例：/疫情资讯
/疫情科普
    防范疫情科普知识
    示例：/疫情科普
/防疫热线 城市
    查询当地防疫热线电话
    示例：/防疫热线 深圳"""


async def get_covid_data(area: str) -> str:
    """
    获取疫情数据
    :param area: 城市
    :return:
    """
    type_ = ""
    result = {}
    msg = ""
    area = area.split()[0]
    # 判断要查询的地区级
    if "省" in area:
        area = area.split("省")[0]
        type_ = "(省)"
    if "市" in area:
        area = area.split("市")[0]
        type_ = "(市)"
    if area in ["北京", "天津", "重庆", "上海"]:
        type_ = "(直辖市)"
    if area in ["香港", "澳门"]:
        type_ = "(特别行政区)"
    if area == "内蒙古自治区":
        area = "内蒙古"
    elif area == "宁夏回族自治区":
        area = "宁夏"
    elif area == "新疆维吾尔自治区":
        area = "新疆"
    elif area == "西藏自治区":
        area = "西藏"
    elif area == "广西壮族自治区":
        area = "广西"
    qqbot.logger.info("正在查询>>>%s%s新冠肺炎疫情最新动态" % (area, type_))
    raw_data = requests.get(covid_url).json()
    # 判断数据拉取状态
    if raw_data["ret"] != 0:
        # 拉取失败
        return "%s%s新冠肺炎疫情最新动态获取失败" % (area, type_)
    else:
        # 拉取成功
        qqbot.logger.info("%s%s新冠肺炎疫情最新动态获取成功,数据解析中" % (area, type_))
        # 解析数据包
        data = raw_data["data"]["diseaseh5Shelf"]
        tree = data["areaTree"]
        all_province = tree[0]["children"]
        if area in ("中国", "国内"):
            qqbot.logger.info("检测到获取国内数据,数据处理中")
            data.pop("areaTree")
            msg += "———国内新冠肺炎疫情最新动态———\n\n"
            msg += "🟠 现存确诊(含港澳台)：{} + {}\n".format(
                data["chinaTotal"]["nowConfirm"], data["chinaAdd"]["confirm"]
            )
            msg += "🟣 现存无症状：{} + {}\n".format(
                data["chinaTotal"]["noInfect"], data["chinaAdd"]["noInfect"]
            )
            if data["chinaAdd"]["localConfirmH5"] > 0:
                msg += "🔵 国内现存确诊：{} + {}\n".format(
                    data["chinaTotal"]["localConfirmH5"],
                    data["chinaAdd"]["localConfirmH5"],
                )
            else:
                msg += "🔵 国内现存确诊：{}\n".format(data["chinaAdd"]["localConfirmH5"])
            msg += "🟡 累计确诊：{}\n".format(data["chinaTotal"]["confirm"])
            msg += "🟢 累计治愈：{}\n".format(data["chinaTotal"]["heal"])
            msg += "🔴 累计死亡：{}\n".format(data["chinaTotal"]["dead"])

            return msg

        for province in all_province:
            if province["name"] == area:
                # 省疫情
                result = province
                if province["name"] in ["内蒙古", "广西", "西藏", "宁夏", "新疆"]:
                    type_ = "(自治区)"
                else:
                    type_ = "(省)"
                break
            for city in province["children"]:
                if city["name"] == area:
                    result = city
                    type_ = "(市)"
        try:
            qqbot.logger.info("检测到获取%s%s数据,数据处理中" % (area, type_))
            msg += "— {}{}新冠肺炎疫情最新动态 —\n\n".format(
                area, type_
            )
            if result["today"]["confirm"] > 0:
                msg += "🔵 现存确诊：{} + {}\n".format(
                    result["total"]["nowConfirm"], result["today"]["confirm"]
                )
            else:
                msg += "🔵 现存确诊：0\n"
            if type_ != "(市)":
                if result["today"]["wzz_add"] > 0:
                    msg += "🟣 现存无症状：{} + {}\n".format(
                        result["total"]["wzz"], result["today"]["wzz_add"]
                    )
                else:
                    msg += "🟣 现存无症状：0 \n"
            msg += "🟡 累计确诊：{}\n".format(result["total"]["confirm"])
            try:
                msg += f"🔴 累计死亡：{result['total']['dead']} ({(result['total']['dead'] / result['total']['confirm'] * 100):.2f}%)\n"
                msg += f"🟢 累计治愈：{result['total']['heal']} ({(result['total']['heal'] / result['total']['confirm'] * 100):.2f}%)\n"
            except ZeroDivisionError:
                msg += f"🔴 累计死亡：{result['total']['dead']}\n"
                msg += f"🟢 累计治愈：{result['total']['heal']}\n"
            if result["today"]["isUpdated"]:
                msg += "⏳  更新时间：{}".format(data["lastUpdateTime"])
            else:
                msg += "⏳  更新时间：当日暂无更新"
            qqbot.logger.info("数据处理成功, %s%s最新疫情消息已发送" % (area, type_))
        except KeyError as e:
            msg = ""
            qqbot.logger.info("未找到%s%s最新疫情消息, 已发送疫情助手菜单" % (area, type_))
    return msg


async def get_grade_data(area: str) -> str:
    """
    获取风险地区
    :param area:
    :return:
    """
    type_ = ''
    area = area.split()[0]
    if "省" in area:
        area = area.split("省")[0]
        type_ = "(省)"
    if "市" in area:
        area = area.split("市")[0]
        type_ = "(市)"
    if area in ["北京", "天津", "重庆", "上海"]:
        type_ = "(直辖市)"
    if area in ["香港", "澳门"]:
        type_ = "(特别行政区)"
    if area == "内蒙古自治区":
        area = "内蒙古"
    elif area == "宁夏回族自治区":
        area = "宁夏"
    elif area == "新疆维吾尔自治区":
        area = "新疆"
    elif area == "西藏自治区":
        area = "西藏"
    elif area == "广西壮族自治区":
        area = "广西"
    qqbot.logger.info("正在查询>>>%s新冠肺炎疫情风险地区" % area)
    try:
        payload_json = {
            "args": {"req": {}},
            "service": "PneumoniaTravelNoAuth",
            "func": "queryAllRiskLevel",
            "context": {"userId": "a"},
        }
        risk_area_data = requests.post(url=grade_url, json=payload_json)
        risk_area_data = risk_area_data.json()
        risk_area_data = risk_area_data["args"]["rsp"]
        qqbot.logger.info("%s新冠肺炎疫情风险地区获取成功, 正在解析中" % area)
        medium_risk_area_list = risk_area_data["mediumRiskAreaList"]
        high_risk_area_list = risk_area_data["highRiskAreaList"]

        msg = "—{}{}新冠肺炎疫情最新动态—\n\n🔰 中风险地区：".format(area, type_)
        mid_risk_msg = ""
        for i in medium_risk_area_list:
            for j in i["list"]:
                if j["cityName"] in [area, area + "市"]:
                    mid_risk_msg += f"\n🪐 {j['areaName']} \n🏠 {j['communityName']}\n"
        if len(mid_risk_msg) > 0:
            mid_risk_msg = mid_risk_msg.replace("、", "\n🏠 ")
            msg += "\n" + mid_risk_msg + "\n"
        else:
            msg += "暂无风险地区\n——————————————————\n\n"

        msg += "🔰 高风险地区："
        high_risk_msg = ""
        for i in high_risk_area_list:
            for j in i["list"]:
                if j["cityName"] in [area, area + "市"]:
                    high_risk_msg += f"\n🪐 {j['areaName']} \n🏠 {j['communityName']}\n"
        if len(high_risk_msg) > 0:
            high_risk_msg = high_risk_msg.replace("、", "\n🏠 ")
            msg += "\n" + high_risk_msg + "\n"
        else:
            msg += "暂无风险地区"
        qqbot.logger.info("数据处理成功, %s新冠肺炎疫情风险地区已发送" % area)
        return msg
    except Exception as e:
        qqbot.logger.info("数据有误, 请重新尝试获取")
        return "数据获取有误, 请尝试重新获取"


async def get_news_data():
    """
    获取新冠肺炎最新资讯
    :return:
    """
    qqbot.logger.info("正在获取新冠肺炎疫情最新资讯动态")
    raw_data = requests.get(news_url).text
    raw_data = json.loads('['+raw_data+']')[0]
    if raw_data['ResultCode'] != '0':
        # 拉取失败
        qqbot.logger.info("新冠肺炎疫情最新资讯动态获取失败")
        return "新冠肺炎疫情最新资讯动态获取失败"
    else:
        data = raw_data['Result'][0]['items_v2'][0]['aladdin_res']['DisplayData']['result']['items']
        qqbot.logger.info("新冠肺炎疫情最新资讯获取成功,正在解析中")
        data_append = []
        for i in range(len(data)):
            if i < 5:
                update_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(data[i]['eventTime'])))
                msg = '📰 资讯详情\n> ' + data[i]['eventDescription'] + '\n🗞️ 更新来源：' + data[i]['siteName'] + '\n⏳ 更新时间：' + update_time
                msg += '\n——————————————————\n\n'
                data_append.append(msg)
        qqbot.logger.info('数据处理成功, 新冠肺炎疫情最新资讯动态已发送')
    return "———新冠肺炎疫情最新资讯动态———\n\n" + "".join(data_append)


async def get_policy(area: str) -> str:
    """
    出行政策单个
    :param area: 城市
    :return:
    """
    url_city_list = 'https://r.inews.qq.com/api/trackmap/citylist?'
    city_list_raw = requests.get(url_city_list)
    city_list = city_list_raw.json()
    msg = ""
    from_id = ''
    to_id = ''
    area = area.split()[0]
    if city_list['status'] == 0 and city_list['message'] == "success":
        for province in city_list['result']:
            for city in province['list']:
                if area == city['name']:
                    from_id = city['id']
    else:
        msg += "城市列表请求错误"
        return msg

    try:
        url_get_policy = f"https://r.inews.qq.com/api/trackmap/citypolicy?&city_id={from_id}"
    except UnboundLocalError:
        msg += "城市名错误"
        return msg

    policy_raw = requests.get(url_get_policy)
    policy = policy_raw.json()
    if policy['status'] == 0 and policy['message'] == "success":
        try:
            data_leave = policy['result']['data'][0]
            msg += f"{area}离开政策：\n{data_leave['leave_policy'].strip()}\n于{data_leave['leave_policy_date']}更新\n\n"
            msg += f"{area}出入政策：\n"
            msg += f"{data_leave['back_policy'].strip()}\n于{data_leave['back_policy_date']}更新\n\n"
            msg += f"{area}酒店政策：{data_leave['stay_info'].strip()}\n\n"
            msg += "免责声明：以上所有数据来源于腾讯新闻出行防疫政策查询"
        except IndexError:
            msg = ''
    else:
        msg += "政策请求错误"
    return msg


async def get_policys(from_city: str, to_city: str) -> str:
    """
    双向出行政策
    :param from_city: 出发城市
    :param to_city: 抵达城市
    :return:
    """
    url_city_list = 'https://r.inews.qq.com/api/trackmap/citylist?'
    city_list_raw = requests.get(url_city_list)
    city_list = city_list_raw.json()
    msg = ""
    from_id = ''
    to_id = ''
    from_city = from_city.split()[0]
    to_city = to_city.split()[0]
    if city_list['status'] == 0 and city_list['message'] == "success":
        for province in city_list['result']:
            for city in province['list']:
                if from_city == city['name']:
                    from_id = city['id']
                if to_city == city['name']:
                    to_id = city['id']
    else:
        msg += "城市列表请求错误"
        return msg

    try:
        url_get_policy = f"https://r.inews.qq.com/api/trackmap/citypolicy?&city_id={from_id},{to_id}"
    except UnboundLocalError:
        msg += "城市名错误"
        return msg

    policy_raw = requests.get(url_get_policy)
    policy = policy_raw.json()
    if policy['status'] == 0 and policy['message'] == "success":
        try:
            data_leave = policy['result']['data'][0]
            data_to = policy['result']['data'][1]
            if from_city == to_city and data_leave['leave_policy'].strip() == data_to['back_policy'].strip():
                msg += f"{from_city}出入政策：\n"
                msg += f"{data_to['back_policy'].strip()}\n于{data_to['back_policy_date']}更新\n\n"
                msg += "\n"
            else:
                msg += f"{from_city}离开政策：\n{data_leave['leave_policy'].strip()}\n于{data_leave['leave_policy_date']}更新\n\n"
                msg += f"{to_city}进入政策：\n{data_to['back_policy'].strip()}\n于{data_to['back_policy_date']}更新\n\n"
            msg += f"{to_city}酒店政策：{data_to['stay_info'].strip()}\n\n"
            msg += "免责声明：以上所有数据来源于腾讯新闻出行防疫政策查询"
        except IndexError:
            msg = ''
    else:
        msg += "政策请求错误"
    return msg


async def get_covid_phone(area: str) -> str:
    """
    防疫热线
    :param area: 城市
    :return:
    """
    msg = ''
    area = area.split()[0]
    if os.path.exists('data.dt'):
        with open('data.dt', 'r', encoding='utf-8') as c:
            res = c.read()
    else:
        res = requests.get('https://heihaoma.com/i-fangyi').text
        with open('data.dt', 'w+', encoding='utf-8') as c:
            c.write(res)
    content = BeautifulSoup(res, 'html.parser')
    data_first = content.find('div', attrs={'id': 'container'})
    data_two = data_first.find_all('li')
    data_append = []
    for city_data in data_two:
        city_name = city_data.find('div', attrs={'class': 'contact-tit'}).text
        city_phone = city_data.find('div', attrs={'class': 'contact-phone'}).text
        data_append.append("☎️ " + city_name + '：' + city_phone)
    for data_phone in data_append:
        if area in data_phone:
            msg += '\n' + data_phone
    return f'————— {area}防疫热线 —————\n' + msg
