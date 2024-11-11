
自建EPG需求

请用python语言实现以下有关epg节目单抓取的程序：
1. 从以下地址抓取频道列表文件：http://210.13.21.3/epgcategory/6000004422.json

2. 在6000004422.json中，提取每一条记录的以下信息：
   "code": "00000001000000050000000000000152",
  "code2": "1",
       "title": "CCTV-1高清",

 "code": "00000001000000050000000000000477",
        "code2": "2",
 "title": "CCTV-2高清",


3. 根据code生成每一个频道的当天的节目单文件下载地址，格式为：http://210.13.21.3/schedules/00000001000000050000000000000152_yyyymmdd.json，
 例如：
 http://210.13.21.3/schedules/00000001000000050000000000000152_20241106.json，
 http://210.13.21.3/schedules/00000001000000050000000000000477_20241106.json
 然后将所有的节目单文件下载到本地
 然后将前七天和后两天的所有频道的节目单文件下载到本地，例如今天是2024年11月6日，则将从2024年10月31日到2024年11月9日的所有频道的节目单文件下载到本地
4.以xml格式生成epg文件，文件名为ee.xml文件，格式如下：
 文件头部内容为：
 <?xml version="1.0" encoding="UTF-8"?>
 <tv info-name="by spark " info-url="https://epg.112114.xyz">
 之后为每个频道的信息及其当天的节目单：
 第一个频道第一部分为频道信息：
 <channel id="1">
        <display-name lang="zh">CCTV-1高清</display-name>
    </channel>
 第一个频道的第二部分为节目单内容：
 <programme channel="1" start="20241106010000 +0800" stop="20241106012800 +0800">
          <title lang="zh">今日说法</title>
     </programme>
     <programme channel="1" start="20241106012800 +0800" stop="20241106015000 +0800">
          <title lang="zh">人口</title>
 </programme>
 .
 .
 .
 之后按照这个格式依次添加所有频道的频道信息及其对应的节目单信息：
 <channel id="2">
        <display-name lang="zh">CCTV-2高清</display-name>
    </channel>
    <programme channel="2" start="20241106000300 +0800" stop="20241106004500 +0800">
        <title lang="zh">对话-2024-43</title>
    </programme>
    <programme channel="2" start="20241106004500 +0800" stop="20241106014500 +0800">
        <title lang="zh">欢乐大猜想</title>
    </programme>
    <programme channel="2" start="20241106014500 +0800" stop="20241106022000 +0800">
        <title lang="zh">能源浪潮</title>
    </programme>
 .
 .
 .

 其中：channel id对应节目单文件中"channel"中的"channelnum”，programme channel对应节目单文件中"channel"中的"channelnum”，start对应节目单文件中的"starttime”，stop对应节目单文件中的"endtime”，<title lang="zh">对应节目单文件中的"schedules"中的”title”
 另外，做以下频道名称的替换：
 CCTV-1高清 替换为 CCTV1
 CCTV-2高清 替换为 CCTV2
 CCTV-3高清 替换为 CCTV3
 CCTV-4高清 替换为 CCTV4
 CCTV-5高清 替换为 CCTV5
 CCTV-6高清 替换为 CCTV6
 CCTV-7高清 替换为 CCTV7
 CCTV-8高清 替换为 CCTV8
 CCTV-9高清 替换为 CCTV9
 CCTV-10高清 替换为 CCTV10
 CCTV-11高清 替换为 CCTV11
 CCTV-12高清 替换为 CCTV12
 CCTV-13高清 替换为 CCTV13
 CCTV-14高清 替换为 CCTV14
 CCTV-15高清 替换为 CCTV15
 CCTV-16高清 替换为 CCTV16
 CCTV-17高清 替换为 CCTV17
 CCTV-5+  替换为 CCTV5+
 BRTV北京卫视高清  替换为 北京卫视
 BRTV文艺高清 替换为  北京文艺
 BRTV纪实科教高清  替换为 北京纪实科教
 BRTV影视高清  替换为 北京影视
 BRTV财经高清  替换为 北京财经
 BRTV体育休闲高清  替换为 北京体育休闲
 BRTV生活高清  替换为 北京生活
 BRTV新闻高清  替换为 北京新闻

5. 将ee.xml压缩为gz格式的压缩文件

其中，以下代码请加上注释：
# Step 2: 提取频道信息
channel_data = []
for channel in channels:
    code = channel.get("code")  #北京联通频道编码
    code2 = channel.get("code2")    #频道编号
    title = channel.get("title")    #频道名称
    channel_data.append({"code": code, "code2": code2, "title": title})
