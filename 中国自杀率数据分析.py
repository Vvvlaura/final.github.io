# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 14:28:26 2023

@author: dell
"""

import folium
import pandas as pd
import requests
import geopandas
import branca
import branca.colormap
import math
from folium.features import GeoJsonPopup, GeoJsonTooltip
import streamlit as st
from streamlit_folium import st_folium
import json

#读取中国各省份自杀率csv文件
china_suicide=pd.read_csv('C:/Users/dell/Desktop/期末/input/suicide_index.csv',encoding="gbk").set_index("Province")

#访问中国各省份json文件
#利用requests包中的get(url)函数，用于返回请求的响应
req = requests.get('https://geo.datav.aliyun.com/areas_v2/bound/100000_full.json')
req.encoding = 'utf-8'
result = json.loads(req.text)

#在json文件中添加各省份的自杀指数信息
#将json文件和自杀率dataframe文件中各省份的名称相对应
for index, item in enumerate(result['features']):
    for i in china_suicide.index:
        if i in item['properties']["name"]:
            result['features'][index]['properties']['Suicide_index']=china_suicide.loc[i]["Suicide_index"]
            result['features'][index]['properties']['Name']=i

#创建含各省份及各省份自杀率数据的列表
suicide_list=[]
province=china_suicide.index.tolist()
statistic=china_suicide["Suicide_index"].tolist()
for i in range(len(province)):
    suicide_list.append((province[i],statistic[i]))
            
#读取中国各省份经纬度文件
province_coordinate = pd.read_csv('C:/Users/dell/Desktop/期末/input/China_states_coordinates.csv',encoding='gbk')

#将中国各省份的json文件转换成geodataframe
#地理坐标系转换成EPSG:4326
china_pro=geopandas.GeoDataFrame.from_features(result, crs="EPSG:4326")
province_merged=china_pro.merge(province_coordinate,how="left",left_on="Name",right_on="States")

#创建colormap
colormap = branca.colormap.LinearColormap(
    vmin=int(math.floor(min(statistic))),
    vmax=int(math.ceil(max(statistic))),
    colors=["red", "orange", "lightblue", "green", "darkgreen"],
    caption="Suicide_index"
)

#设置popup
popup = GeoJsonPopup(
    fields=["Name", "Suicide_index"],
    aliases=["省份：", "自杀指数："],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

#设置tooltip
tooltip = GeoJsonTooltip(
    fields=["Name", "Suicide_index"],
    aliases=["省份：", "自杀指数："],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

#创建底图
chinam = folium.Map(location=[35, 105], zoom_start=4)
#添加颜色表、popup和tooltip
g = folium.GeoJson(
    province_merged,
    style_function=lambda x: {
        "fillColor": colormap(x['properties']["Suicide_index"])
        if x['properties']["Suicide_index"] is not None
        else "transparent",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.4,
    },
    tooltip=tooltip,
    popup=popup,
).add_to(chinam)

folium.LayerControl(collapsed=True).add_to(chinam)
colormap.add_to(chinam)

st.title("中国各省份自杀率地图")
st.markdown("基于百度指数关键词爬取")
#显示中国各省份自杀率地图
st_folium(chinam,width=1200,height=500)