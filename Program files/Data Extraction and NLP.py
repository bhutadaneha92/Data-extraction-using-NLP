import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Read an Excel file into a pandas DataFrame
df = pd.read_excel('C:/Users/Admin/Desktop/20211030 Test Assignment/Input.xlsx', sheet_name = "Sheet1")

i=0
for url in df.iloc[:,1]:
    
    req_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    req = requests.get(url, headers=req_headers)
    #print(req.status_code)
    #Create BeautifulSoup object
    soup = BeautifulSoup(req.content, "html.parser")

    #Extract Article Title
    Article_tag = soup.find("title")            #with tag

    Article_title = soup.find("title").string   #only article
    
    filename = str(int(df.iloc[i,0]))
    i=i+1

    #Check the file is alredy present or not
    isFile = os.path.isfile(filename)
    if isFile == True:
        file = open(filename + ".txt","r", encoding="utf-8")
    elif isFile == False:
        file = open(filename + ".txt","a",encoding="utf-8")
        file.write(Article_title + "\n")

        #Extract Article Text
        paragraphs = soup.find_all("p")
        for data in paragraphs:
            Article_text = data.get_text()
            file.writelines(Article_text)
file.close()
    
    
