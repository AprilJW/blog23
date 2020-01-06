"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, HttpRequest, JsonResponse
import post
from post import urls as p_urls
import user
from user import urls as u_urls


# def index(request):
#     """视图函数:请求进来返回响应"""
#     response = HttpResponse(b'hello magedu')
#     print(response.charset) # utf-8
#     return response


# http://localhost:8000/?a=100&b=abc
def index(request:HttpRequest):
    """视图函数:请求进来返回响应"""
    print(request.GET)  # 查询字符串?a=100&b=abc print(request.POST)
    print(request.session)
    print(request.COOKIES)
    print('-' * 30)
    keys = ('method', 'path_info', 'GET', 'POST')  # 重要属性
    items = dict(filter(lambda x: x[0] in keys, request.__dict__.items()))
    return JsonResponse(items)


def test(request, username, id):
    print(type(username), type(id))
    return HttpResponse(
        'hello test page.username={}:{}, id={}:{}'.format(
            username, type(username).__name__, id, type(id).__name__))



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    #path('index', index), # index可以匹配;index/不能匹配
    path('index/', index),  # index index/都可以匹配;index/a不能匹配
    path('test/<username>/<int:id>', test),  # /test/tom/2 实参注入
    path('users/', include('user.urls')),
    # path('post/', p_urls),
    # path('posts/', include('post/urls'))
    # path('admin/', user.urls),

]
