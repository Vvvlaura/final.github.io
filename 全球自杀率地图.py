# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 09:29:38 2023

@author: dell
"""
import pandas as pd
import streamlit as st
import requests
import geopandas
import branca
import math
import folium
from folium.features import GeoJsonPopup, GeoJsonTooltip
from streamlit_folium import st_folium

st.title("全球各国平均自杀率地图")
#读取全球各国自杀率文件
df = pd.read_csv("C:/Users/dell/Desktop/期末/input/suicide.csv")
#修改列名
df.columns = ['Country','Year','Probability of dying(Both sexes)','Probability of dying(Male)',
          'Probability of dying(Female)','Suicide rate(Both sexes)','Suicide rate(Male)','Suicide rate(Female)']
#得到各国的男性、女性和总的自杀率数据
df['Probability of dying(Both sexes)']=df['Probability of dying(Both sexes)'].str[0:4].astype(float)
df['Probability of dying(Female)']=df['Probability of dying(Female)'].str[0:4].astype(float)
df['Probability of dying(Male)']=df['Probability of dying(Male)'].str[0:4].astype(float)
df['Suicide rate(Both sexes)']=df['Suicide rate(Both sexes)'].str[0:4].astype(float)
df['Suicide rate(Female)']=df['Suicide rate(Female)'].str[0:4].astype(float)
df['Suicide rate(Male)']=df['Suicide rate(Male)'].str[0:4].astype(float)

#得到各国的平均男性、女性和总的自杀率
df=df.groupby('Country')[['Probability of dying(Both sexes)','Probability of dying(Male)','Probability of dying(Female)',
'Suicide rate(Both sexes)','Suicide rate(Male)','Suicide rate(Female)']].mean()

#以各国总自杀率为标准降序排列，设置数据表格的颜色
suicide_show=df.sort_values('Suicide rate(Both sexes)',ascending=False).style.background_gradient(cmap='Blues')
#在streamlit网页中显示
st.write(suicide_show)

#获取全球各国经纬度信息
country = pd.read_csv('C:/Users/dell/Desktop/期末/input/world_country.csv')
#得到全球各国经纬度和自杀率的数据表格信息
merged_df = pd.merge(country,df, on='Country', how='inner')[["Country","Suicide rate(Male)","Suicide rate(Female)","Suicide rate(Both sexes)","longitude","latitude"]]

#访问全球各国json文件
#利用requests包中的get(url)函数，用于返回请求的响应
response = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json"
)
data = response.json()

#将全球各国的json文件转换成geodataframe
#地理坐标系转换成EPSG:4326
countryjson = geopandas.GeoDataFrame.from_features(data, crs="EPSG:4326")
countrymerge=countryjson.merge(merged_df,how="left",left_on="name", right_on="Country")

#基于总自杀率创建colormap
colormap = branca.colormap.LinearColormap(
    vmin=math.floor(countrymerge["Suicide rate(Both sexes)"].min()),
    vmax=math.ceil(countrymerge["Suicide rate(Both sexes)"].max()),
    colors=["red", "orange", "lightblue", "green", "darkgreen"],
    caption="Suicide rate(Both sexes)"
)

#创建popup
popup = GeoJsonPopup(
    fields=["Country", "Suicide rate(Both sexes)","Suicide rate(Male)","Suicide rate(Female)"],
    aliases=["Country", "Suicide rate(Both sexes)","Suicide rate(Male)","Suicide rate(Female)"],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

#创建tooltip
tooltip = GeoJsonTooltip(
    fields=["Country", "Suicide rate(Both sexes)","Suicide rate(Male)","Suicide rate(Female)"],
    aliases=["Country", "Suicide rate(Both sexes)","Suicide rate(Male)","Suicide rate(Female)"],
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
m = folium.Map(zoom_start=10)
#添加colormap，tooltip和popup
folium.GeoJson(
    countrymerge,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"]["Suicide rate(Both sexes)"])
        if x["properties"]["Suicide rate(Both sexes)"] is not None
        else "transparent",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.4,
    },
    tooltip=tooltip,
    popup=popup,
).add_to(m)
folium.LayerControl(collapsed=True).add_to(m)
colormap.add_to(m)

#在streamlit网页中显示
st_folium(m,width=1200,height=500)