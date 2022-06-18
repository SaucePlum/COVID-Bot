<div align="center">

![botpy](https://socialify.git.ci/ReadSmall/COVID-Bot/image?description=1&font=Source%20Code%20Pro&forks=1&issues=1&language=1&logo=https%3A%2F%2Fgithub.com%2Ftencent-connect%2Fbot-docs%2Fblob%2Fmain%2Fdocs%2F.vuepress%2Fpublic%2Ffavicon-64px.png%3Fraw%3Dtrue&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light)

[![Language](https://img.shields.io/badge/language-python-green.svg?style=plastic)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg?style=plastic)](https://github.com/ReadSmall/COVID-Bot/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![PyPI](https://img.shields.io/pypi/v/qq-botpy)
[![BK Pipelines Status](https://api.bkdevops.qq.com/process/api/external/pipelines/projects/qq-guild-open/p-713959939bdc4adca0eea2d4420eef4b/badge?X-DEVOPS-PROJECT-ID=qq-guild-open)](https://devops.woa.com/process/api-html/user/builds/projects/qq-guild-open/pipelines/p-713959939bdc4adca0eea2d4420eef4b/latestFinished?X-DEVOPS-PROJECT-ID=qq-guild-open)

_✨ QQ频道机器人-疫情助手 ✨_

[爱发电](https://afdian.net/@nian-bot)
·
[开发者频道](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=1MVLD4&appChannel=share&businessType=9&from=246610&biz=ka)

</div>

## 机器人指令

    /疫情 城市
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
        示例：/防疫热线 深圳

## 使用方法

使用代码库前需要配置好相关的信息，可以跟随下面的步骤进行

### 环境安装

py包的依赖配置，通过`pip install -r requirements.txt` 可以安装所有的依赖包

### 运行机器人

在代码库根目录执行下面命令

```shell
python3 bot.py
```

## 代码说明

    .
    ├── LICENSE
    ├── README.md
    ├── .gitignore 
    ├── util.py             # 字符相关的处理
    ├── command_register.py # 指令的装饰器处理
    ├── requirements.txt    # py包的依赖配置，通过`pip install -r requirements.txt` 可以安装所有的依赖包
    ├── bot.py              # 程序运行入口，包括不同指令的处理

## 特别感谢

-   [Python SDK](https://github.com/tencent-connect/botpy) 为疫情助手开发提供SDK

## 免责声明

数据来源：  

-   [腾讯新闻疫情API](https://news.qq.com/zt2020/page/feiyan.htm#/)  提供疫情查询服务
-   [腾讯风险等级API](https://news.qq.com/zt2020/page/feiyan.htm#/)  提供疫情风险地区查询服务
-   [百度疫情资讯API](https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner)  提供疫情资讯服务
-   [腾讯出行政策API](https://news.qq.com/hdh5/sftravel.htm#/)  提供出行政策服务
-   [黑号码防疫热线API](https://heihaoma.com/i-fangyi)  提供防疫热线电话服务

