#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
util.py: 疫情助手核心

Author: NianGui
Time  : 2022/4/23 1:01
"""
import json
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
    示例：/疫情科普"""


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
            msg += "\t\t🇨🇳国内新冠肺炎疫情最新动态🇨🇳\n===========================\n"
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
            msg += "\t\t{}{}新冠肺炎疫情最新动态\n===========================\n".format(
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
            msg += f"🔴 累计死亡：{result['total']['dead']} ({(result['total']['dead'] / result['total']['confirm'] * 100):.2f}%)\n"
            msg += f"🟢 累计治愈：{result['total']['heal']} ({(result['total']['heal'] / result['total']['confirm'] * 100):.2f}%)\n"
            if result["today"]["isUpdated"]:
                msg += "⏳︎ 最后更新时间：\n     {}".format(data["lastUpdateTime"])
            else:
                msg += "⏳︎ 最后更新时间：当日暂无更新"
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
        mediumRiskAreaList = risk_area_data["mediumRiskAreaList"]
        highRiskAreaList = risk_area_data["highRiskAreaList"]

        msg = "\t\t\t\t{}{}风险地区信息\n===========================\n中风险地区: ".format(area, type_)
        mid_risk_msg = ""
        for i in mediumRiskAreaList:
            for j in i["list"]:
                if j["cityName"] in [area, area + "市"]:
                    mid_risk_msg += f"{j['areaName']} {j['communityName']}\n"
        if len(mid_risk_msg) > 0:
            mid_risk_msg = mid_risk_msg.replace("、", "\n")
            msg += "\n" + mid_risk_msg + "\n"
        else:
            msg += "暂无风险地区\n"

        msg += "高风险地区: "
        high_risk_msg = ""
        for i in highRiskAreaList:
            for j in i["list"]:
                if j["cityName"] in [area, area + "市"]:
                    high_risk_msg += f"{j['areaName']} {j['communityName']}\n"
        if len(high_risk_msg) > 0:
            high_risk_msg = high_risk_msg.replace("、", "\n")
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
                msg = data[i]['eventDescription'] + '\n更新来源: ' + data[i]['siteName'] + '\n更新时间: ' + update_time
                msg += '\n===========================\n'
                data_append.append(msg)
        qqbot.logger.info('数据处理成功, 新冠肺炎疫情最新资讯动态已发送')
    return "新冠肺炎疫情最新资讯动态\n===========================\n" + "".join(data_append)


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
            msg += f"{area}离开政策：{data_leave['leave_policy'].strip()}\n于{data_leave['leave_policy_date']}更新\n\n"
            msg += f"{area}出入政策：\n"
            msg += f"{data_leave['back_policy'].strip()}\n于{data_leave['back_policy_date']}更新\n\n"
            msg += f"{area}酒店政策：\n{data_leave['stay_info'].strip()}\n\n"
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
                msg += f"{from_city}离开政策：{data_leave['leave_policy'].strip()}\n于{data_leave['leave_policy_date']}更新\n\n"
                msg += f"{to_city}进入政策：\n{data_to['back_policy'].strip()}\n于{data_to['back_policy_date']}更新\n\n"
            msg += f"{to_city}酒店政策：\n{data_to['stay_info'].strip()}\n\n"
            msg += "免责声明：以上所有数据来源于腾讯新闻出行防疫政策查询"
        except IndexError:
            msg = ''
    else:
        msg += "政策请求错误"
    return msg

# 失效
async def get_covid_phone(area: str) -> str:
    """
    防疫热线
    :param area: 城市
    :return:
    """
    msg = ''
    area = area.split()[0]
    res = requests.get('https://heihaoma.com/i-fangyi').text
    content = BeautifulSoup(res, 'html.parser')
    data_first = content.find('div', attrs={'id': 'container'})
    data_two = data_first.find_all('li')
    data_append = []
    for city_data in data_two:
        city_name = city_data.find('div', attrs={'class': 'contact-tit'}).text
        city_phone = city_data.find('div', attrs={'class': 'contact-phone'}).text
        data_append.append(city_name + '：' + city_phone)
    for data_phone in data_append:
        if area in data_phone:
            msg += data_phone + '\n'
    return msg
