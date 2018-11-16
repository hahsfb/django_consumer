#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : get_areas_data.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-11-14 下午4:25
@Version : 
@Description : 从中国统计局获取中国省市区信息及code,并且写成sql语句
"""
import requests
from bs4 import BeautifulSoup
domain_name = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/'

index = 'index.html'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'AD_RS_COOKIE=20081945; _trs_uv=jogng78m_6_66nz',
    'Host': 'www.stats.gov.cn',
    'If-Modified-Since': 'Thu, 05 Jul 2018 00:43:11 GMT',
    'If-None-Match': "17b5-57035d4e665c0-gzip",
    'Referer': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
}


def get_utf_8(req):
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding
        return req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；


province = requests.get(url=domain_name + index, headers=headers)
sql = "INSERT INTO `admin_areas` VALUES ({}, {}, {}, {}, '{}', '{}');"
# INSERT INTO `admin_areas` VALUES (330000, 330000, 330000, 1, '浙江省', '浙江省');
# INSERT INTO `admin_areas` VALUES (330100, 330000, 330100, 2, '杭州市', '浙江省杭州市');
# INSERT INTO `admin_areas` VALUES (330101, 330000, 330100, 3, '市辖区', '浙江省杭州市市辖区');
province = get_utf_8(province)
soup = BeautifulSoup(province, 'html.parser')
for link in soup.select("table.provincetable > tr.provincetr > td > a"):
    # print(link.get('href'), ' ====> ', link.text)
    code = str(link.get('href')[:3:] + '0000')
    code = code.replace('.', '')
    print(sql.format(code, code, code, 1, link.text, link.text))

    city = requests.get(url=domain_name + link.get('href'), headers=headers)
    city = get_utf_8(city)
    soup_city = BeautifulSoup(city, 'html.parser')
    for link_city in soup_city.select("table.citytable > tr.citytr"):
        link_city = link_city.select('td > a')
        city_code = str(link_city[0].text[:6:])
        print(sql.format(city_code, code, city_code, 2, link_city[1].text, link.text+link_city[1].text))

        area = requests.get(url=domain_name + link_city[1].get('href'), headers=headers)
        area = get_utf_8(area)
        soup_area = BeautifulSoup(area, 'html.parser')
        for link_area in soup_area.select("table.countytable > tr.countytr"):
            link_area_a = link_area.select('td > a')
            if link_area_a:
                link_area = link_area_a
            else:
                link_area = link_area.select('td')
            area_code = str(link_area[0].text[:6:])
            print(sql.format(area_code, code, city_code, 3, link_area[1].text, link.text + link_city[1].text + link_area[1].text))


