from django.shortcuts import render
import pandas as pd
import os 
from django.conf import settings
import json
import requests
from bs4 import BeautifulSoup
import folium
from geopy.geocoders import Nominatim
import re
from django.http import JsonResponse
import numpy as np
# Create your views here.

def index(request):
    # C:\Users\ITSC\Desktop\방방콕콕\data
    # C:\Users\ITSC\Desktop\방방콕콕\intro\views.py
    path = "intro\\data\\지자체 주요관광.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    choice = pd.read_csv(absolute_path)
    arr = np.random.randint(0, 390, 10)
    # choice = choice.head(5)    
    choice = choice.rename(columns={
        "관광지":"title",        
        
    })
    choice = choice.sample(n=10, replace=True)
    print(choice)
    choice_str = choice.loc[:,["title","image_url","category","군구"]].to_json(orient="records", force_ascii=False)
    choice_json = json.loads(choice_str)
    
    
    
    path = "intro\\data\\지자체 주요관광.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    search = pd.read_csv(absolute_path)
    # # print(search.head(10))
    search = search
    search = search.rename(columns={
        "관광지":"title",        
    })
    search_str = search.loc[:,["title","image_url"]].to_json(orient="records", force_ascii=False)
    search_json = json.loads(search_str)
    
    
    
    
    context = {
        "choice" : choice_json    ,
        "search" : search_json
        
    }
    return render(request,"index.html",context)

def detail(request, local):
    local = local.strip()
    path = "intro\\data\\지자체 주요관광.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    choice = pd.read_csv(absolute_path)
    choice = choice[choice["관광지"]==local]
    # print(choice["image_url"],"           11111111111111")
    
    choice = choice.rename(columns={
        "관광지":"title",
        
    })
    
    
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(local)
    
    
    # # print(local)
    
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": "KakaoAK "+"33a8a1ace17ab4332bcbb8ece4495a19",
        "content-type": "application/json;charset=UTF-8"
    }
    regex = "\(.*\)|\s-\s.*"
    local = re.sub(regex, '', local)
    # print(local)
    params = {
        "query" : local
    }
    
    data_list = requests.get(url, params=params, headers=headers).json()["documents"]
    

    x = data_list[0]["x"]
    y = data_list[0]["y"]
    print(data_list[0])
    map = folium.Map(location=[y,x],zoom_start=15, width='100%', height='100%')
    folium.Marker([y,x], popup= local).add_to(map)
    maps= map._repr_html_()
    
    address = data_list[0]["address_name"].split(" ")
    print("add1",address)
    address = address[0]
    print("add2",address)
    match address:
        case "강원특별자치도":
            address = "강원"
        case "강원도":
            address = "강원"
        case "전북특별자치도":
            address = "전북"
        case "전라북도":
            address = "전북"
        case "전남특별자치도":
            address = "전남"
        case "전라남도":
            address = "전남"
    print("1111",address)
    
    
    path = "intro\\data\\merge.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    df = pd.read_csv(absolute_path)
    df.rename(columns={"기초지자체 방문자 수":"방문자수"},inplace=True)
    pie = df[df["광역지자체명"] == address][["기초지자체명", "방문자수"]].sort_values(by='방문자수', ascending=False)
    pie_str = pie.loc[:,["기초지자체명","방문자수"]].to_json(orient="records", force_ascii=False)
    
    path = "intro\\data\\지자체 주요관광지점 입장객.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    df = pd.read_csv(absolute_path)
    line_str = df[df["관광지"].str.contains(local)].iloc[0,7:].to_json(orient="records", force_ascii=False)
    print(line_str)
    
    
    path = "intro\\data\\merge.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    df = pd.read_csv(absolute_path)
    df.rename(columns={"인당 지출액":"지출액"},inplace=True)
    df_str = df.loc[:,["광역지자체명","지출액"]].groupby("광역지자체명").mean().reset_index().to_json(orient="records", force_ascii=False)
    
    print("111111111"+data_list[0]["address_name"])
    
    context = {
        "j" : choice,
        "map" : maps,
        "address" : data_list[0]["address_name"],
        "pie" : pie_str,
        "line" : line_str,
        "bar" : df_str,
        "local" : local,
        
        
    }
    return render(request, "detail.html",context)

def check(request):
    # print(request.body)
    data = json.loads(request.body)
    # print(data["do"])
    do = data["do"]    
    
    path = "intro\\data\\지자체 주요관광.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    df = pd.read_csv(absolute_path)
    # print(df.head(20))
    df = df[df["시도"].str.contains(do[0]) & df["시도"].str.contains(do[1])]
    
    df_str = df.loc[:,["관광지","image_url"]].head(20).to_json(orient="records", force_ascii=False)
    df_json = json.loads(df_str)
    # # print("df_str",df.loc[:,["관광지","image_url"]].head(20))
    
    return JsonResponse({
        "list" : df_json
    })

def tag(request, tagName):
    path = "intro\\data\\지자체 주요관광.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    df = pd.read_csv(absolute_path)
    df = df[df["category"] == tagName]
    df = df.rename(columns={
        "관광지":"title",        
        
    })
    df_str = df.to_json(orient="records", force_ascii=False)
    df_json = json.loads(df_str)
    context = {
        "lists" : df_json,
        "tag" : tagName,
    }
    return render(request, "tag.html", context)