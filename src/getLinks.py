# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

#initialise dataframe
df=pd.DataFrame(columns=['link','text','state','sender','date'])

#how many pages to cycle through?
counts=range(1,21)

#for each page
for count in counts:
    
    #what URL are we scraping from?
    url='https://www.whatdotheyknow.com/body/mhclg?page='+str(count)
    
    #get the HTML page
    response = requests.get(url)
     
    #apply bs parser
    soup = BeautifulSoup(response.text, "html.parser")
     
    #find all divs
    divs=soup.findAll('div')
    
    #for each div
    for div in divs:
        
        #use 'try' block to handle the exception where div has no 'class'
        try:
            
            #if the div is a request listing
            if div['class']==['request_listing']:
                
                #we're interested in the following chuck of  html:
                content1=div.contents[1]
                
                #get all the links
                links = content1.findAll('a')
                
                #the first  link is the question
                link_href='https://www.whatdotheyknow.com'+links[0]['href']
                link_text=links[0].text
                
                #the 'state' of a request is in a 'strong' tag
                strong=content1.findAll('strong')
                state=strong[0].text
                
                #clean the 'state' by getting rid of double spaces
                while '  ' in state:
                    state=state.replace('  ',' ')
                
                #get rid of full stop in state
                state=state.replace('.','')
                
                #extract date andtime
                time=content1.findAll('time')
                datetime=time[0]['title'][:-6]
                
                #the send is the third link
                sender=links[2].text
                
                #put everythingin a dataframe
                df_row = pd.DataFrame([[link_href, link_text, state, sender, datetime]], columns=df.columns)
        
                #add dataframe to our list
                df=df.append(df_row, ignore_index=True)
        
        except:
            pass

#convert 'date' column to pandas datetime        
df['date']= pd.to_datetime(df['date'])

#export to csv
df.to_csv('../output/whatDoTheyKnow_links.csv',index=False)