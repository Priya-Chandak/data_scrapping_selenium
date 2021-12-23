#!/usr/bin/env python
# coding: utf-8

# ### Data Scrapping for Delhi - Paint Dealers from multiple brands from the website : 
# "https://www.dealerservicecenter.in/"
# 

# In[ ]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import re


# In[ ]:


options = webdriver.ChromeOptions() 
driver = webdriver.Chrome(executable_path=r'{"path_to_your_chromedrive"}/chromedriver.exe')

name1=[]
address1=[]
contact1=[]
dealers1=[]

paint_dealers=['asian-paints','british-paints','dulux','kansai-nerolac','nippon-paint','shalimar','mrf','indigo-paints']

for i in range(0,len(paint_dealers)):
    url = "https://www.dealerservicecenter.in/list/paint/{}/delhi/delhi".format(paint_dealers[i])
    
    driver.get(url)
    r = requests.get(url)  
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.findAll('div',{'class':'panel panel-default testimonial'})
    print(url)
    
        
    for j in range(5,len(table)):
        try:
            name = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/h3/a".format(j)).text
            address = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/ul/li[1]".format(j)).text
            contact = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/ul/li[3]".format(j)).text
            name1.append(name)
            address1.append(address)
            contact1.append(contact)
            dealers1.append(paint_dealers[i])
        except Exception as ex:
            name = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/h3/a".format(j+1)).text
            address = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/ul/li[1]".format(j+1)).text
            contact = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/ul/li[3]".format(j+1)).text
            name1.append(name)
            address1.append(address)
            contact1.append(contact)
            dealers1.append(paint_dealers[i])
            print(ex)
        
        


# In[ ]:


df=pd.DataFrame(list(zip(name1,address1,contact1,dealers1)),columns=['Name','Address','Contact','Dealer'])
df.head()


# #### By running this script you will get the data for Delhi Paint Dealers for the brands mentioned above 

# In[ ]:


name2=[]
address2=[]
contact2=[]
dealers2=[]

paint_dealers=['asian-paints','british-paints','dulux','kansai-nerolac','nippon-paint','shalimar','mrf','indigo-paints']

for i in range(0,len(paint_dealers)):
    url = "https://www.dealerservicecenter.in/list/paint/{}/delhi/new-delhi".format(paint_dealers[i])
    
    driver.get(url)
    r = requests.get(url)  
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.findAll('div',{'class':'panel panel-default testimonial'})
    print(url)
    
        
    for j in range(5,len(table)):
        try:
            name = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/h3/a".format(j)).text
            address = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/ul/li[1]".format(j)).text
            contact = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/ul/li[3]".format(j)).text
            name2.append(name)
            address2.append(address)
            contact2.append(contact)
            dealers2.append(paint_dealers[i])
        except Exception as ex:
            name = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/h3/a".format(j+1)).text
            address = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/ul/li[1]".format(j+1)).text
            contact = driver.find_element_by_xpath("//*[@id='content']/div/div/div[1]/div/div/div/div[{}]/div/ul/li[3]".format(j+1)).text
            name2.append(name)
            address2.append(address)
            contact2.append(contact)
            dealers2.append(paint_dealers[i])
            print(ex)
        
        


# In[ ]:


df1=pd.DataFrame(list(zip(name2,address2,contact2,dealers2)),columns=['Name','Address','Contact','Dealer'])
df1.head()
len(df1)


# In[ ]:


data=[df,df1]
final_data = pd.concat(data)
final_data.drop_duplicates(inplace=True)
final_data=pd.DataFrame(final_data)
final_data.reset_index(inplace=True)
final_data.drop(columns=['index'],axis=1,inplace=True)
final_data.head()


# In[ ]:


final_data['Address'] = final_data['Address'].map(lambda x: x.lstrip('Address:\n'))
final_data['Contact'] = final_data['Contact'].map(lambda x: x.lstrip('Contact Number:\n').rstrip(' REPORT WRONG NUMBER!'))

final_data.head()


# In[ ]:


final_data['Pincode']=pd.DataFrame(final_data,columns=['Pincode'])
final_data['State']=pd.DataFrame(final_data,columns=['State'])

for i in range(0,len(final_data)):
    final_data['State']='Delhi'
final_data.head(10)


# In[ ]:


a=[]
str=final_data['Address']

for i in str:
    
    if re.findall(r'- (\d{6})', i):
        x=re.findall(r'- (\d{6})', i)
        if x[0] in i:
            start_index = i.index(x[0])
            s= i[start_index:start_index+6]
            a.append(s)
            
    else :
        a.append('--')
    

final_data['Pincode'] = pd.DataFrame(a)
final_data


# In[ ]:


final_data.to_excel('path/file_name.xlsx',index=False)

