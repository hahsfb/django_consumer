from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'index.html', {'tag': "good!!!"})
    # return HttpResponse("Hello world ! ")
