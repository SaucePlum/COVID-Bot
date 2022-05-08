# QQ频道机器人-疫情助手

该代码库是基于QQ机器人框架进行开发的机器人，用于服务查询国内疫情最新动态、疫情资讯、风险地区、出行政策、疫情科普、防疫热线等服务

赞助开发者：[爱发电](https://afdian.net/@nian-bot)

开发者频道：[点击加入开发者QQ频道](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=1MVLD4&appChannel=share&businessType=9&from=246610&biz=ka)

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

## 使用方法

使用代码库前需要配置好相关的信息，可以跟随下面的步骤进行

### 环境安装

py包的依赖配置，通过`pip install -r requirements.txt` 可以安装所有的依赖包

### 环境配置

拷贝根目录的 `config.example.yaml` 为 `config.yaml`

```shell
cp config.example.yaml config.yaml
```

修改 `config.yaml` ，填入自己的 BotAppID 和 Bot token 以及其他相关参数，参数介绍如下

```shell
token:
  appid: "123" # 机器人appid
  token: "xxx" # 机器人token
```

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
    ├── config.example.yaml # 配置文件模版
    ├── config.yaml         # 实际的读取配置文件（需要自己从demo复制一份修改参数）
    ├── util.py             # 字符相关的处理
    ├── command_register.py # 指令的装饰器处理
    ├── requirements.txt    # py包的依赖配置，通过`pip install -r requirements.txt` 可以安装所有的依赖包
    ├── bot.py              # 程序运行入口，包括不同指令的处理

## 特别感谢

-   [油价助手](https://github.com/wzpan/oil-price-bot/) 为疫情助手提供指令注册
-   [Python SDK](https://github.com/tencent-connect/botpy) 为疫情助手开发提供SDK

## 免责声明

数据来源：  

-   [腾讯新闻疫情API](https://news.qq.com/zt2020/page/feiyan.htm#/)  提供疫情查询服务
-   [腾讯风险等级API](https://news.qq.com/zt2020/page/feiyan.htm#/)  提供疫情风险地区查询服务
-   [百度疫情资讯API](https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner)  提供疫情资讯服务
-   [腾讯出行政策API](https://news.qq.com/hdh5/sftravel.htm#/)  提供出行政策服务
-   [黑号码防疫热线API](https://heihaoma.com/i-fangyi)  提供防疫热线电话服务

