# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


df=pd.DataFrame(columns=['link','text','state','sender','date'])

counts=range(1,21)

for count in counts:
    url='https://www.whatdotheyknow.com/body/mhclg?page='+str(count)
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
     
    divs=soup.findAll('div')
    
    for div in divs:
        try:
            if div['class']==['request_listing']:
                
                content1=div.contents[1]
                
                links = content1.findAll('a')
                href='https://www.whatdotheyknow.com'+links[0]['href']
                link_text=links[0].text
                
                strong=content1.findAll('strong')
                state=strong[0].text
                while '  ' in state:
                    state=state.replace('  ','')
                state=state.replace('.','')
                
                time=content1.findAll('time')
                datetime=time[0]['title'][:-6]
                
                sender=links[2].text
                
                df_row = pd.DataFrame([[href, link_text, state, sender, datetime]], columns=df.columns)
        
                df=df.append(df_row, ignore_index=True)
        
        except:
            pass
        
df['date']= pd.to_datetime(df['date'])
df.to_csv('whatDoTheyKnow_links.csv',index=False)