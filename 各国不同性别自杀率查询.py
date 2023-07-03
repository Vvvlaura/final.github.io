# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 10:00:52 2023

@author: dell
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("各国不同性别自杀率查询")
#读取各国自杀率文件
df = pd.read_csv("C:/Users/dell/Desktop/期末/input/master.csv")
#修改列名
df.rename(columns={"suicides/100k pop":"suicides_pop","HDI for year":"HDI_for_year",
              " gdp_for_year ($) ":"gdp_for_year"," gdp_per_capita ($) ":"gdp_per_capita",
                "gdp_per_capita ($)":"gdp_per_capita"}, inplace=True)

#获取国家列表
data1=df.drop_duplicates("country",keep="last",inplace=False)
country_list=data1["country"].tolist()

#使用multiselect(label, options)函数用于创建下拉多选框，返回选中元素列表（可选元素为国家）
countries_gender = st.multiselect('选择国家',country_list)

#获取男性和女性自杀率dataframe文件
df_male=df[df["sex"]=="male"]
df_female=df[df["sex"]=="female"]
fig, ax = plt.subplots()

#遍历选中的元素列表
for country in countries_gender:
    #返回选中国家的男性各年份自杀人数和总人口数据
    exp_male = df_male["country"]==country
    records_male=df_male[exp_male]
    records_male=records_male.groupby("year")[["suicides_no","population","suicides_pop"]].sum()
    #返回选中国家的女性各年份自杀人数和总人口数据
    exp_female=df_female["country"]==country
    records_female=df_female[exp_female]
    records_female=records_female.groupby("year")[["suicides_no","population","suicides_pop"]].sum()
    #返回各年份列表
    years=records_female.index.tolist()
    #选中国家男性各年份自杀人数列表
    suicide_male_num=records_male["suicides_no"].values.tolist()
    #选中国家男性各年份总人口列表
    population_male_num=records_male["population"].values.tolist()
    #选中国家女性各年份自杀人数列表
    suicide_female_num=records_female["suicides_no"].values.tolist()
    #选中国家女性各年份总人口列表
    population_female_num=records_female["population"].values.tolist()
    male_list=[]
    female_list=[]
    #利用自杀人数/总人口计算自杀率
    #统计女性各年份平均自杀率
    for i in range(len(records_female)):
        m=round((suicide_female_num[i]/population_female_num[i])*100000,2)
        female_list.append(m)
    #计算男性各年份平均自杀率
    for i in range(len(records_male)):
        m=round((suicide_male_num[i]/population_male_num[i])*100000,2)
        male_list.append(m)
    #男性各年份平均自杀率折线图
    ax.plot(years,male_list,label=country+":"+"male",marker=".")
    #女性各年份平均自杀率折线图
    ax.plot(years,female_list,label=country+":"+"female",marker="^")
#添加x轴和y轴名称
plt.xlabel("year")
plt.ylabel("suicide_rate")
#添加图例
plt.legend(loc=3)
st.pyplot(fig)