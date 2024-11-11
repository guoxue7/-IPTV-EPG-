import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import gzip

# Step 1: 抓取频道列表文件
channel_list_url = "http://210.13.21.3/epgcategory/6000004422.json"
response = requests.get(channel_list_url)
channels_data = response.json()["epgCategorydtl"]

# Step 2: 提取频道信息并应用替换规则
channel_replacements = {
    "CCTV-1高清": "CCTV1", "CCTV-2高清": "CCTV2", "CCTV-3高清": "CCTV3", "CCTV-4高清": "CCTV4",
    "CCTV-5高清": "CCTV5", "CCTV-6高清": "CCTV6", "CCTV-7高清": "CCTV7", "CCTV-8高清": "CCTV8",
    "CCTV-9高清": "CCTV9", "CCTV-10高清": "CCTV10", "CCTV-11高清": "CCTV11", "CCTV-12高清": "CCTV12",
    "CCTV-13高清": "CCTV13", "CCTV-14高清": "CCTV14", "CCTV-15高清": "CCTV15", "CCTV-16高清": "CCTV16",
    "CCTV-17高清": "CCTV17", "CCTV-5+": "CCTV5+", "BRTV北京卫视高清": "北京卫视", "BRTV文艺高清": "北京文艺",
    "BRTV纪实科教高清": "北京纪实科教", "BRTV影视高清": "北京影视", "BRTV财经高清": "北京财经",
    "BRTV体育休闲高清": "北京体育休闲", "BRTV生活高清": "北京生活", "BRTV新闻高清": "北京新闻"
}

channel_data = []
for channel in channels_data:
    code = channel.get("code")  #北京联通频道编码
    code2 = channel.get("code2")    #频道编号
    title = channel.get("title")    #频道名称
    title = channel_replacements.get(title, title)  # 应用替换规则
    channel_data.append({"code": code, "code2": code2, "title": title})

# Step 3: 下载前7天和后2天的节目单文件
all_schedules = {}
date_range = [datetime.now() + timedelta(days=i) for i in range(-7, 3)]

for channel in channel_data:
    channel_schedules = []
    for date in date_range:
        date_str = date.strftime("%Y%m%d")
        schedule_url = f"http://210.13.21.3/schedules/{channel['code']}_{date_str}.json"
        try:
            response = requests.get(schedule_url)
            response.raise_for_status()
            schedule_data = response.json().get("schedules", [])
            for program in schedule_data:
                channel_schedules.append({
                    "channelnum": channel["code2"],
                    "starttime": program["starttime"],
                    "endtime": program["endtime"],
                    "title": program["title"]
                })
        except requests.RequestException as e:
            print(f"Failed to download schedule for {channel['title']} on {date_str}: {e}")
    all_schedules[channel["code2"]] = channel_schedules

# Step 4: 生成XML文件
tv = ET.Element("tv", {
    "info-name": "by spark",
    "info-url": "https://epg.112114.xyz"
})

# 添加频道信息
for channel in channel_data:
    channel_element = ET.SubElement(tv, "channel", id=channel["code2"])
    ET.SubElement(channel_element, "display-name", lang="zh").text = channel["title"]

# 添加节目单信息
for channel_id, schedules in all_schedules.items():
    for program in schedules:
        start_time = datetime.strptime(program["starttime"], "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S") + " +0800"
        end_time = datetime.strptime(program["endtime"], "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S") + " +0800"
        programme_element = ET.SubElement(tv, "programme", {
            "channel": channel_id,
            "start": start_time,
            "stop": end_time
        })
        ET.SubElement(programme_element, "title", lang="zh").text = program["title"]

# 保存为XML文件
tree = ET.ElementTree(tv)
with open("ee.xml", "wb") as f:
    tree.write(f, encoding="UTF-8", xml_declaration=True)

# Step 5: 压缩为gz文件
with open("ee.xml", "rb") as f_in, gzip.open("ee.xml.gz", "wb") as f_out:
    f_out.writelines(f_in)

print("EPG XML文件已生成并压缩为ee.xml.gz。")
