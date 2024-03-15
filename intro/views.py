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
    
    
    
    context = {
        "choice" : choice_json    
    }
    return render(request,"index.html",context)

def detail(request, local):
    return render(request, "detail.html")