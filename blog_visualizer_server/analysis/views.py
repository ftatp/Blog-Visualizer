from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	if request.method == "POST":
		print(request.POST)

	return HttpResponse("Hello, world. You're at the polls index.")
