# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 13:28:10 2023

@author: dell
"""


import pandas as pd
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from msedge.selenium_tools import EdgeOptions
import time

#获取cookie值
def get_cookie(url):
    edge_options=EdgeOptions()
    #限制图片加载
    edge_options.use_chromium=True
    No_Image_loading={"profile.managed_default_content_settings.images": 2}
    edge_options.add_experimental_option("prefs",No_Image_loading)
    #限制JavaScript执行
    edge_options.add_argument("--disable-javascript")
    # 创建浏览器对象
    s = Service(executable_path=r'D:/msedgedriver.exe')
    browser = webdriver.Edge(service=s)
    browser.get(url)
    browser.find_element(By.CSS_SELECTOR,"span.username-text").click()
    #获取cookie值
    print("等待登录...")
    #输入账号和密码登录
    while True:
        if browser.find_element(By.CSS_SELECTOR,"span.username-text").text != "登录":
           break
        else:
           time.sleep(3)
    #登录后显示“登录成功”的提示
    print("已登录，现在为您保存cookie...")
    #将cookie值保存至'cookies.txt'文件
    with open('cookies.txt', 'w', encoding='u8') as f:
        json.dump(browser.get_cookies(), f)
    #关闭浏览器
    browser.close()
    print("cookie保存完成，游览器已自动退出...")

#爬取百度指数有关“自杀”这一关键词的各省份搜索数据
def get_data(url):
    #全国各省份列表
    l0=['安徽','澳门','北京','重庆','福建','广东','广西','甘肃','贵州']
    l1=['河北','黑龙江','河南','湖南','湖北','海南','吉林','江苏','江西']
    l2=['辽宁','内蒙古','宁夏','青海','上海','四川','山东','山西','陕西']
    l3=['天津','台湾','西藏','香港','新疆','云南','浙江']
    suicide_index={}
    #利用selenium打开浏览器和百度指数“自杀”相关搜索的网页
    s = Service(executable_path=r'D:/msedgedriver.exe')
    browser = webdriver.Edge(service=s)
    #利用获得的cookie值登录百度指数网站
    with open('cookies.txt', 'r', encoding='u8') as f:
       cookies = json.load(f)
    browser.get(url)
    for cookie in cookies:
       browser.add_cookie(cookie)
    browser.get(url)
    #设置等待时间（此处设置为5秒）
    time.sleep(5)
    #采集网页中关于各省份“自杀”搜索指数日均值的信息
    for i in range(1,10):
      #通过xpath表达式查找并返回“全国”按钮
      button=browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/button")
      #执行click()操作
      browser.execute_script("arguments[0].click();",button)
      time.sleep(2)
      #循环查找并返回各省份按钮
      button2=browser.find_element(By.XPATH,"/html/body/div[5]/div/div/div[2]/div[2]/span[{}]".format(i))
      #执行click()操作，返回动态生成的网页
      browser.execute_script("arguments[0].click();",button2)
      #循环查找并返回“所有城市”按钮
      button3=browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/button/span[1]")
      #执行click()操作，返回动态生成的网页
      browser.execute_script("arguments[0].click();",button3)
      #设置等待时间（此处设置为3秒）
      time.sleep(3)
      #通过xpath表达式查找并返回搜索指数整体日均值
      index=int(browser.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr/td[2]/div').text.replace(",",""))
      #添加到字典中
      suicide_index[l0[i-1]]=index
      #print(browser.find_element(By.XPATH,"/html/body/div[5]/div/div/div[5]/div[2]/span[{}]".format(i)).text)
      browser.get(url)
      time.sleep(2)
    for i in range(1,10):
      button=browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/button")
      browser.execute_script("arguments[0].click();",button)
      time.sleep(2)
      button2=browser.find_element(By.XPATH,"/html/body/div[5]/div/div/div[3]/div[2]/span[{}]".format(i))
      browser.execute_script("arguments[0].click();",button2)
      button3=browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/button/span[1]")
      browser.execute_script("arguments[0].click();",button3)
      time.sleep(3)
      index=int(browser.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr/td[2]/div').text.replace(",",""))
      suicide_index[l1[i-1]]=index
      #print(browser.find_element(By.XPATH,"/html/body/div[5]/div/div/div[5]/div[2]/span[{}]".format(i)).text)
      browser.get(url)
      time.sleep(2)
    for i in range(1,10):
      button=browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/button")
      browser.execute_script("arguments[0].click();",button)
      time.sleep(2)
      button2=browser.find_element(By.XPATH,"/html/body/div[5]/div/div/div[4]/div[2]/span[{}]".format(i))
      browser.execute_script("arguments[0].click();",button2)
      button3=browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/button/span[1]")
      browser.execute_script("arguments[0].click();",button3)
      time.sleep(3)
      index=int(browser.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr/td[2]/div').text.replace(",",""))
      suicide_index[l2[i-1]]=index
      #print(browser.find_element(By.XPATH,"/html/body/div[5]/div/div/div[5]/div[2]/span[{}]".format(i)).text)
      browser.get(url)
      time.sleep(2)
    for i in range(1,8):
      button=browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/button")
      browser.execute_script("arguments[0].click();",button)
      time.sleep(2)
      button2=browser.find_element(By.XPATH,"/html/body/div[5]/div/div/div[5]/div[2]/span[{}]".format(i))
      browser.execute_script("arguments[0].click();",button2)
      button3=browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/button/span[1]")
      browser.execute_script("arguments[0].click();",button3)
      time.sleep(3)
      index=int(browser.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr/td[2]/div').text.replace(",",""))
      suicide_index[l3[i-1]]=index
      #print(browser.find_element(By.XPATH,"/html/body/div[5]/div/div/div[5]/div[2]/span[{}]".format(i)).text)
      browser.get(url)
      time.sleep(2)
    return suicide_index

#获取中国各省份人口信息
def load_chinapop(path):
    #读取中国各省份人口文件
    china_population = pd.read_csv(path,encoding="gbk")
    #设置“Province Name”列为索引值
    china_population=china_population.set_index("PROVINCE NAME")
    #返回得到的中国各省份人口数据列表
    return china_population

#统计计算各省份自杀率指数
def suicide(suicide_index,china_population):
    #创建空字典
    suicide={}
    #遍历循环省份数据
    for i in suicide_index:
       for j in china_population.index:
           if i==j:
               #通过自杀搜索指数日均值/总人口统计自杀率指数
               index=suicide_index[i]/china_population.loc[i]["POPULATION"]
               suicide[i]=round(index*(10**6),2)
    #返回各省份自杀率指数字典
    return suicide

#获取含中国各省份名称和自杀率指数的数据列表
def china_suicide(suicide):
    china_suicide=pd.DataFrame(list(suicide.items()),columns=["Province","Suicide_index"])
    #设置省份名称为索引值
    china_suicide=china_suicide.set_index("Province")
    return china_suicide

#获取中国各省份人口信息
path_chinapop='china_provinces_population.csv'
china_population=load_chinapop(path_chinapop)

#获取cookie值
url_cookie='https://index.baidu.com/v2/index.html'
get_cookie(url_cookie)

#爬取百度指数有关“自杀”这一关键词的各省份搜索数据
url_browser='https://index.baidu.com/v2/main/index.html#/trend/%E8%87%AA%E6%9D%80?words=%E8%87%AA%E6%9D%80'
suicide_index=get_data(url_browser)

#统计计算各省份自杀率指数
suicide=suicide(suicide_index,china_population)

#获取含中国各省份名称和自杀率指数的数据列表
china_merge=china_suicide(suicide)

#保存中国各省份名称和自杀率指数的数据列表为csv文件
china_merge.to_csv('suicide_index.csv', encoding= 'gbk')
