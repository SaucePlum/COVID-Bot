#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
util.py: 疫情助手核心

Author: NianGui
Time  : 2022/4/23 1:01
"""

import qqbot
import requests

# 疫情数据API > 腾讯
covid_url = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf"
# 风险地区API > 腾讯
grade_url = "https://wechat.wecity.qq.com/api/PneumoniaTravelNoAuth/queryAllRiskLevel"


def get_menu():
    return """
/疫情 城市
    查询指定城市当天疫情数据
    示例： /疫情 深圳
/风险地区 城市
    查询国内风险地区
    示例： /风险地区 深圳
"""


def get_covid_data(area: str) -> str:
    qqbot.logger.info('正在查询 %s 的疫情消息' % area)
    # 应该不会有人闲到写全称吧
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
    type_ = ""  # 标记是省还是市
    result = {}
    msg = ""
    raw_data = requests.post(url=covid_url)
    raw_data = raw_data.json()
    if raw_data["ret"] != 0:
        qqbot.logger.info("ret不为0，疑似有问题")
    qqbot.logger.info('%s 的疫情消息获取成功,正在解析中' % area)
    data = raw_data["data"]["diseaseh5Shelf"]
    tree = data["areaTree"]
    all_province = tree[0]["children"]
    # 先最特殊情况
    if area in ("中国", "全国", "国内"):
        qqbot.logger.info('包含特殊情况, 正在处理特殊情况')
        data.pop("areaTree")
        msg += f"为你查询到中国疫情：\n"
        msg += f"🟠 现存确诊(含港澳台)：{data['chinaTotal']['nowConfirm']}(+{data['chinaAdd']['confirm']})\n"
        msg += (
            f"🟣 现存无症状：{data['chinaTotal']['noInfect']}(+{data['chinaAdd']['noInfect']})\n"
        )
        msg += (
            f"🔵 境内现存确诊：{data['chinaTotal']['localConfirmH5']}("
            + ("+" if data["chinaAdd"]["localConfirmH5"] > 0 else "")
            + f"{data['chinaAdd']['localConfirmH5']})"
        )  # localConfirm和localConfirmH5不一样，页面显示的是H5
        msg += "\n"
        msg += f"🟡 累计确诊：{data['chinaTotal']['confirm']}\n"
        msg += f"🟢 累计治愈：{data['chinaTotal']['heal']}\n"
        msg += f"🔴 累计死亡：{data['chinaTotal']['dead']}\n"
        return msg
    elif area == "吉林市":
        for province in all_province:
            if province["name"] == "吉林":
                for city in province["children"]:
                    if city["name"] == "吉林":
                        result = city
                        type_ = "(市)"
    else:
        # 移除“市”
        if area[-1] == "市":
            area = area[0:-1]
        # 先找省
        if area[-1] == "省":
            # 针对指定为省份的查询
            for province in all_province:
                if province["name"] == area[0:-1]:
                    province.pop("children")
                    result = province
                    type_ = "(省)"
        else:
            # 不会优化，两个for嗯找，能跑就行
            for province in all_province:
                if province["name"] == area and "省" not in area:
                    # 没有写“省”字，但要找的确实是一个省
                    province.pop("children")
                    result = province
                    type_ = "(省)"
                    break
                for city in province["children"]:
                    if city["name"] == area:
                        result = city
                        type_ = "(市)"
    if area in ["北京", "天津", "重庆", "上海"]:
        type_ = "(直辖市)"
    elif area in ["香港", "澳门"]:
        type_ = "(特别行政区)"
    msg += f"为你查询到{result['name']}{type_}疫情：\n"
    msg += f"🔵 现存确诊：{result['total']['nowConfirm']}" + (
        f"(+{result['today']['confirm']})" if result["today"]["confirm"] > 0 else ""
    )
    msg += "\n"
    if type_ != "(市)":  # api里新增了wzz和wzz_add字段，但是二级行政区恒为0
        try:
            msg += f"🟣 现存无症状：{result['total']['wzz']}" + (
                f"(+{result['today']['wzz_add']})"
                if result["today"]["wzz_add"] > 0
                else ""
            )
            msg += "\n"
        except:
            pass
    msg += f"🟡 累计确诊：{result['total']['confirm']}\n"
    try:
        msg += f"🔴 累计死亡：{result['total']['dead']} ({result['total']['deadRate']}%)\n"
    except:
        msg += f"🔴 累计死亡：{result['total']['dead']} ({(result['total']['dead'] / result['total']['confirm'] * 100):.2f}%)\n"
    try:
        msg += f"🟢 累计治愈：{result['total']['heal']} ({result['total']['healRate']}%)\n"
    except:
        msg += f"🟢 累计治愈：{result['total']['heal']} ({(result['total']['heal'] / result['total']['confirm'] * 100):.2f}%)\n"
    msg += (
        f"🔷 当前地区信息今日已更新\n最后更新时间：\n{data['lastUpdateTime']}\n"
        if result["today"]["isUpdated"]
        else "🔴 当前地区信息今日无更新\n"
    )
    qqbot.logger.info('数据处理成功, %s最新疫情消息已发送' % area)
    if type_ in ["(省)", "(特别行政区)"]:  # 没有获取到风险地区
        return msg
    else:
        return msg


def get_grade_data(area: str) -> str:
    qqbot.logger.info('正在查询 %s 的风险地区' % area)
    try:  # 不知道稳不稳，先用try包一下
        url_risk_area = (
            "https://wechat.wecity.qq.com/api/PneumoniaTravelNoAuth/queryAllRiskLevel"
        )
        payload_json = {
            "args": {"req": {}},
            "service": "PneumoniaTravelNoAuth",
            "func": "queryAllRiskLevel",
            "context": {"userId": "a"},
        }
        risk_area_data = requests.post(url=url_risk_area, json=payload_json)
        risk_area_data = risk_area_data.json()
        risk_area_data = risk_area_data["args"]["rsp"]
        qqbot.logger.info('%s 的风险地区获取成功, 正在解析中' % area)
        mediumRiskAreaList = risk_area_data["mediumRiskAreaList"]
        highRiskAreaList = risk_area_data["highRiskAreaList"]

        # （吉林市上面没移除“市”）
        if area[-1] == "市":
            area = area[0:-1]
        msg = "为你查询{}风险地区\n🟠 中风险地区\n".format(area)
        mid_risk_msg = ""
        for i in mediumRiskAreaList:
            for j in i["list"]:
                if j["cityName"] in [area, area + "市"]:
                    mid_risk_msg += f"  {j['areaName']} {j['communityName']}\n"
        if len(mid_risk_msg) > 0:
            mid_risk_msg = mid_risk_msg.replace("、", "\n  ")
            msg += mid_risk_msg + "\n"
        else:
            msg += "  N/A\n"

        msg += "🔴 高风险地区\n"
        high_risk_msg = ""
        for i in highRiskAreaList:
            for j in i["list"]:
                if j["cityName"] in [area, area + "市"]:
                    high_risk_msg += f"  {j['areaName']} {j['communityName']}\n"
        if len(high_risk_msg) > 0:
            high_risk_msg = high_risk_msg.replace("、", "\n  ")
            msg += high_risk_msg + "\n"
        else:
            msg += "  N/A\n"

        qqbot.logger.info('数据处理成功, %s最新疫情消息已发送' % area)
        return msg
    except:
        qqbot.logger.info('数据有误, 请重新尝试获取' % area)
        return "数据获取有误, 请尝试重新获取"
