# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 20:42:45 2023

@author: dell
"""


import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("自杀率和gdp相关性分析")
fig, ax = plt.subplots()
#读取各国自杀率文件
df = pd.read_csv("C:/Users/dell/Desktop/期末/input/master.csv")
suicide_rate=pd.DataFrame(columns=["suicides_pop","gdp_per_capita"])
#修改列名
df.rename(columns={"suicides/100k pop":"suicides_pop","HDI for year":"HDI_for_year",
              " gdp_for_year ($) ":"gdp_for_year"," gdp_per_capita ($) ":"gdp_per_capita",
                "gdp_per_capita ($)":"gdp_per_capita"}, inplace=True)

#获取各国各年份平均自杀率和gdp文件
suicide_gdp=df[["suicides_pop","gdp_per_capita"]].groupby("gdp_per_capita")["suicides_pop"].mean()
#各国各年份gdp数据
x=suicide_gdp.index.tolist()
#各国各年份平均自杀率数据
y=suicide_gdp.values.tolist()
#创建gdp和自杀率dataframe文件
suicide_rate["gdp_per_capita"]=x
suicide_rate["suicides_pop"]=y

#利用多项式回归基于自杀率和gdp拟合曲线
sns.regplot(x='gdp_per_capita', y='suicides_pop', data=suicide_rate,
             marker='*',
             order=4,#默认为1，越大越弯曲
             scatter_kws={'s': 60,'color':'#016392',},#设置散点属性，参考plt.scatter
             line_kws={'linestyle':'--','color':'#c72e29'}#设置线属性，参考 plt.plot             
             )
plt.show()

#在streamlit网页中显示
st.pyplot(fig)
st.set_option('deprecation.showPyplotGlobalUse', False)