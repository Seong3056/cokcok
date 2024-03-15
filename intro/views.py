from django.shortcuts import render
import pandas as pd
import os 
from django.conf import settings
import json
import requests
from bs4 import BeautifulSoup
# Create your views here.

def index(request):
    # C:\Users\ITSC\Desktop\방방콕콕\data
    # C:\Users\ITSC\Desktop\방방콕콕\intro\views.py
    path = "intro\\data\\2022 top100 데이터.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    choice = pd.read_csv(absolute_path)

    choice = choice.head(5)
    choice = choice.rename(columns={
        "제목":"title",
        "중분류":"category"
    })
    choice_str = choice.loc[:,["title","category"]].to_json(orient="records", force_ascii=False)
    choice_json = json.loads(choice_str)
    
    path = "intro\\data\\20240314091744_표_관광지검색순위.csv"
    absolute_path = os.path.join(settings.BASE_DIR, path)
    search = pd.read_csv(absolute_path,encoding="cp949")
    print(search.head(10))
    search = search
    search = search.rename(columns={
        "관광지명":"title",
        "중분류":"category",
        "주소":"address"
    })
    search_str = search.loc[:,["title","category","address"]].to_json(orient="records", force_ascii=False)
    search_json = json.loads(search_str)
    
    
    context = {
        "choice" : choice_json    ,
        "search" : search_json
        
    }
    return render(request,"index.html",context)

def detail(request, local):
    return render(request, "detail.html")