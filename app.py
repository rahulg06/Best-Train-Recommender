import streamlit as st
import pickle
import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
train_info=pickle.load(open('train_info.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
train_nums=pickle.load(open('train_nums.pkl','rb'))
station_code=pickle.load(open('station_code.pkl','rb'))
st.title('Best Train Recommender')
s=st.selectbox(
     'Select Source Station: ',
     station_code['Station name'].values)
d=st.selectbox(
     'Select Destination Station: ',
     station_code['Station name'].values)
s_idx=0
d_idx=0
for i in range(len(station_code)):
    if(station_code['Station name'][i]==s):
        s_idx=i
    if (station_code['Station name'][i] == d):
        d_idx = i
source=station_code['Station code'][s_idx]
des=station_code['Station code'][d_idx]
train_numbers=[]
def recommend(from_station,to_station):
    API_URL = "https://apis.ausoftwaresolutions.in/v1/train-between-stations/"
    data = {
        "from": from_station,
        "to": to_station,
        "api_key": "2cpmQaxGMoYTynz4UANEI1mwlAsq0fQwqW2OYuOx9SGoGmh2YRCpHet8E8xICTKZoer6x8p5aqsSiMG64UHZz6iLeBspNvZyraXLAxSrRU"
    }
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        output = response.text
    else:
        print("Rahul","Error occurred: ", response.status_code)
    soup=BeautifulSoup(output,'lxml')

    json_data = output
    data = json.loads(json_data)
    #print(data)

    if "found_trains" in data["result"]:
        for train_info in data["result"]["found_trains"].values():
            train_numbers.append(train_info["train_no"])
    index = []
    #print(train_numbers)
    for i in train_numbers:
        for j in range(len(train_nums)):
            if(i==train_nums[j]):
                index.append(j)
        #temp=train_info[train_info['train_no']==i]
        #print(temp)
        #index.append(temp.index[0])
    score = {}
    for i in index:
        score[i] = round(similarity[i].tolist()[0], 2)
    #print(score)
    maxi = 0
    ans = 0
    for i in score:
        if (score[i] > maxi):
            print(i)
            ans = i
            maxi = score[i]
    #print(ans)
    return train_nums[ans]
if st.button('Recommend'):
    try:
        number=recommend(source,des)
        if (number[0] == '0'):
            url = 'https://www.confirmtkt.com/train-ratings-reviews/0%d' % int(number)
        else:
            url = 'https://www.confirmtkt.com/train-ratings-reviews/%d' % int(number)
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'lxml')
        soup.prettify()
        r = soup.find('span', itemprop='itemreviewed')
        st.write("")
        st.write(r.text)

    except:
        st.write("Try with different station!")

    #st.write(r.text)
#print(train_info)
print('exit')
print('rahul')
type(train_info)