# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import bs4, requests, os
import pandas as pd
import numpy as np

inputF = os.path.dirname(os.path.realpath(__file__)) + '/../../output/whatDoTheyKnow_links.csv'
outputF = os.path.dirname(os.path.realpath(__file__)) + '/../../output/'

df = pd.read_csv(inputF)

# print(df.head())

countRecs = 0
    
for ind, i in enumerate(df["link"]):
    if (str(i).find("incoming") > -1) or (str(i).find("outgoing") > -1) or (str(i).find("comment") > -1) :
        print(i)
        # webpage link the FOI request page
        response = requests.get(i)
        # response = requests.get("https://www.whatdotheyknow.com/request/guidance_for_local_authorities_o#incoming-1396660")
    
        # parse html data                 
        parsed_html = bs4.BeautifulSoup(response.text,features='lxml')
        b = parsed_html.findAll("div",attrs={"request-status",})[0]
        outcome = b.find("p").text
        
        #outgoing from the website, incoming from MHCLG
        outgoing = parsed_html.findAll("div",attrs={"outgoing correspondence js-collapsable"})
        incoming = parsed_html.findAll("div",attrs={"incoming correspondence normal js-collapsable"})
        
        # putting all results for an FOI request into a dataframe
        FOI = {}
        FOI['name'] = [i.findAll("span")[0].text for i in incoming]
        FOI['date'] = [i.findAll("time")[0].text for i in incoming]
        FOI['text'] = [i.findAll("div",attrs={"correspondence_text"})[0].text for i in incoming]
        FOI["incoming_outgoing"] = ["incoming" for i in range(len(incoming))]
        
        # putting incoming correspondence into df
        FOI_df = pd.DataFrame(FOI, index = range(len(incoming)))
        
        FOI = {}
        FOI['name'] = [i.findAll("span")[0].text for i in outgoing]
        FOI['date'] = [i.findAll("time")[0].text for i in outgoing]
        FOI['text'] = [i.findAll("div",attrs={"correspondence_text"})[0].text for i in outgoing]
        FOI["incoming_outgoing"] = ["outgoing" for i in range(len(outgoing))]
        
        # append the outgoing correspondence to the df
        FOI_df = FOI_df.append(pd.DataFrame(FOI))
        
        # creating column for the title of the FOI request
        FOI_df["title"] = parsed_html.findAll("h1")[1].text
        
        # attaching outcome
        FOI_df["outcome"] = outcome
        
        # ID for each piece of correspondence in the FOI
        FOI_df["ID"] = np.arange(len(FOI_df))
    
        # save data frame for FOI as pickle and html file
        # print(FOI_df.head())
        # print(i[(i.find("-") + 1):])    
        fileName = str(i[(i.find("-") + 1):])
        
        with open(outputF + fileName + ".html", "w+") as f:
            f.write(str(response.text))
            
        FOI_df.to_pickle(outputF + fileName + ".pickle")
            
        countRecs = countRecs + 1
        
        if countRecs > 20:
            break;



