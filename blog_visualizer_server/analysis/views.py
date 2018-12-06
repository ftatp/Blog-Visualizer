from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import pandas as pd
import json

from analysis import Preprocessing


def stringify_keys(d):
	"""Convert a dict's keys to strings if they are not."""
	for key in d.keys():
		# check inner dict
		if isinstance(d[key], dict):
			value = stringify_keys(d[key])
		else:
			value = d[key]

		# convert nonstring to string if needed
		if not isinstance(key, str):
			try:
				d[str(key)] = value
			except Exception:
				try:
					d[repr(key)] = value
				except Exception:
					raise

			# delete old key
			del d[key]
	return d

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

		data_dict = stringify_keys(data_dict)
		print(json.dumps(data_dict, indent=4, sort_keys=True))
		#print(data_dict)
		return JsonResponse(data_dict)

	return HttpResponse("Hello, world. You're at the index.")
