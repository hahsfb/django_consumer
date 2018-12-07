from django.shortcuts import render
from django.http import HttpResponse
from app.models import Test
# Create your views here.


def index(request):
    return render(request, 'index.html', {'tag': "good!!!"})
    # return HttpResponse("Hello world ! ")


# 数据库操作
def testdb(request):
    test1 = Test(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")
