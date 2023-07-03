# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 00:23:05 2023

@author: dell
"""
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("各国不同年龄段自杀率查询")
#读取全球各国自杀率文件
data=pd.read_csv("C:/Users/dell/Desktop/期末/input/master.csv")
#获取国家列表
data1=data.drop_duplicates("country",keep="last",inplace=False)
country_list=data1["country"].tolist()

#使用multiselect(label, options)函数用于创建下拉多选框，返回选中元素列表（可选元素为国家）
countries_age = st.multiselect('选择国家',country_list)
fig, ax = plt.subplots()

#遍历选中的元素列表
for country in countries_age:
    #返回选中国家的数据表格信息
    exp = data["country"]==country
    records=data[exp]
    #选中国家各年龄段的自杀人数和总人口数据
    age=records.groupby("age")[["suicides_no","suicides/100k pop","population"]].sum()
    #选中国家各年龄段的自杀人数列表
    suicide_num=age["suicides_no"].values.tolist()
    #选中国家各年龄段总人口列表
    population_num=age["population"].values.tolist()
    #利用自杀人数/总人口计算自杀率
    #统计各年龄段平均自杀率数据
    new_list=[]
    for i in range(len(suicide_num)):
        m=round((suicide_num[i]/population_num[i])*100000,2)
        new_list.append(m)
    #各年龄段平均自杀率折线图
    ax.plot(age.index.tolist(),new_list,label=country,marker="^")

#设置x轴、y轴坐标和图例
plt.xlabel("age")
plt.ylabel("suicide_rate")
plt.legend(loc=3)

#在streamlit网页中显示
st.pyplot(fig)