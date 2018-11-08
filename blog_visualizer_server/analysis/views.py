from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import pandas as pd

@csrf_exempt
def index(request):
	if request.method == "POST":
		print(request.POST)
		
		data_csv = pd.read_csv("static/cluster_mean.csv")
		data_dict = data_csv.T.to_dict()
		print(data_dict)


		#return HttpResponse("hello!! " + request.POST['search_list'])
		return JsonResponse(data_dict)

	return HttpResponse("Hello, world. You're at the index.")
