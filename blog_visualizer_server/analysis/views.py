from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	if request.method == "POST":
		print(request.POST)
		
		return HttpResponse("hello!! " + request.POST['search_list'])
#return JsonResponse({"kk": "aaaa"})

	return HttpResponse("Hello, world. You're at the index.")
