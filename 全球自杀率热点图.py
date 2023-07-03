# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 13:09:39 2023

@author: dell
"""

import pandas as pd
import streamlit as st
import requests
import geopandas
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


st.title("全球男性和女性平均自杀率热点图")
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
suicide_show=df.sort_values('Suicide rate(Male)',ascending=False).style.background_gradient(cmap='Blues')
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

#构造函数创建可动态播放的热力图图层
heat_data_male = [[row['latitude'], row['longitude'], row['Suicide rate(Male)']] for index, row in merged_df.iterrows()]
heat_data_female = [[row['latitude'], row['longitude'], row['Suicide rate(Female)']] for index, row in merged_df.iterrows()]

# 创建地图
male = folium.Map(zoom_start=7,width=600,height=400)
female = folium.Map(zoom_start=7,width=600,height=400)

#添加男性自杀率热力图
HeatMap(heat_data_male).add_to(male)
#添加女性自杀率热力图
HeatMap(heat_data_female).add_to(female)

st.header("全球男性自杀率热点图")
st_folium(male,width=1200,height=500)
st.header("全球女性自杀率热点图")
st_folium(female,width=1200,height=500)