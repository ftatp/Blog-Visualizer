from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import pandas as pd
import re
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

def parse_url_to_id(url):
	pattern1 = re.compile("//blog.naver.com/")
	pattern2 = re.compile(".blog.me/")

	search1 = pattern1.search(url)
	search2 = pattern2.search(url)

	url_splited = url.split('/')
	
	if search1 != None:
		return url_splited[-2], url_splited[-1]
	elif search2 != None:
		for fragment in url_splited:
			print("--------------fragment---------------", fragment)
			print(re.search(".blog.me$", fragment))
			if bool(re.search(".blog.me$", fragment)):
				print("!@#$!@#!@#!#!#!")
				return re.sub(".blog.me$", '', fragment), url_splited[-1]

	return None, None


@csrf_exempt
def index(request):
	if request.method == "POST":
		url = request.POST.get("url")
		print(url)

		data_csv = pd.read_csv("static/cluster_mean.csv")
		User_id = 'newpark314'
		Post_id = '221387605004'

		User_id, Post_id = parse_url_to_id(url)
		print(User_id, Post_id)

#Category = '맛집'
		post_data = Preprocessing.get_naver_post_all_data(User_id, Post_id)#User_id, Post_id, Category)
		cluster_dict = data_csv.T.to_dict()
		
		data_dict = {
			'post': post_data,
			'clusters': cluster_dict
		}

		data_dict = stringify_keys(data_dict)
		print(json.dumps(data_dict['post'], indent=4, sort_keys=True))
		print("--------------------------------------------------------\n\n\n")
		#print(data_dict)
		return JsonResponse(data_dict)

	return HttpResponse("Hello, world. You're at the index.")
