from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import pandas as pd

#from analysis import Main_data_preprocessing_20181106 as preprocesser

from konlpy.tag import Kkma


from analysis import Preprocessing

# coding: utf-8

# In[29]:

from bs4 import BeautifulSoup 
import re
import requests
from selenium import webdriver
from pykospacing import spacing
import pandas as pd
from konlpy.tag import Kkma
import numpy as np
import pickle




@csrf_exempt
def index(request):
	if request.method == "POST":
		print(request.POST)
		
		data_csv = pd.read_csv("static/cluster_mean.csv")
		User_id = 'newpark314'
		Post_id = '221387605004'
		Category = '맛집'

		post_data = Preprocessing.get_naver_post_all_data()#User_id, Post_id, Category)
		cluster_dict = data_csv.T.to_dict()
		
		data_dict = {
			'post': post_data,
			'clusters': cluster_dict
		}
		print("hdfgx")
		print(data_dict)

		#return HttpResponse("hello!! " + request.POST['search_list'])
		return JsonResponse(data_dict)

	return HttpResponse("Hello, world. You're at the index.")
