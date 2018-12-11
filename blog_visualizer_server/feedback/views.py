from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os


@csrf_exempt
def index(request):
	if request.method == "POST":
		print("feedback: ", request.POST)
		time = datetime.today().strftime("%Y%m%d%H%M%S")
		uid, pid = request.POST.get("uid"), request.POST.get("pid")
		feedback = request.POST.get("feedback")

		csv_name = 'static/data_collector.csv'
		col_name = "\t".join(["time", "uid", "pid", "label"])
		if not os.path.exists(csv_name):
			with open(csv_name, 'w') as f:
				f.write(col_name + '\n')
		content = "\t".join([time, uid[0], pid[0], feedback[0]])
		print("content: ", content)
		with open(csv_name, 'a', encoding='utf-8') as f:
			f.write(content + "\n")

	return HttpResponse("Thank you for your feedback")
