from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from messages import Messages
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse
import simplejson
from django.views.decorators.http import require_GET, require_POST
from functools import wraps
from utils.messages import Messages
from django.contrib.auth.admin import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate


# request.user.is_authenticated


def require_POST1(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse(Messages.BAD_REQUEST)
        return func(request, *args, **kwargs)

    return wrapper


# Django本身的login_required1，（当用户没有登陆时）会在服务器端跳转（redirect），
# 不适合前后端分离，所以自己实现装饰器
def login_required1(viewfunc):
    @wraps
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return viewfunc(request, *args, **kwargs)
        return HttpResponse(status=401)

    return wrapper


@require_POST1
def userlogin(request: HttpRequest):
    try:
        userload = simplejson.loads(request.body)
        username = userload['username']
        password = userload['password']
        user = authenticate(username=username, password=password)
        if user:
            print(type(user), user)
        else:
            return JsonResponse(Messages.INVALID_USERNAME_OR_PASSWORD)
    except Exception as e:
        print(e)
        return JsonResponse(Messages.INVALID_USERNAME_OR_PASSWORD)


# 登出之后，用户必须重新登录获得sessionid，该id已经彻底清除了，
# 包括数据库django_session表的记录。
@login_required1
def userlogout(request: HttpRequest):
    print(type(request.user), request.user)
    print(*request.session.items())  # 好多内容

    del request.session['user_info']  # 删除user_info信息
    logout(request)
    # logout会移除request.user，清除session，清除数据库django_session记录
    # 总结，这个sessionid找不到数据库记录了，彻底作废了
    print('-' * 30)
    print('-' * 30)

    print(type(request.user), request.user)  # 匿名用户
    print(*request.session.items())  # 空

    return JsonResponse({}, status=204)


# def get_condition(arg):
#     dict1 = {'con1': arg < 1,
#              'con2': arg < 20 and arg > 101
#             }
#     if arg < 1:
#         arg = 1
#     if arg < 20 and arg > 101:
#         arg = 20
#     return arg
#
#
#
# def inspect_arg(arg, get_condition, request):
#     try:
#         arg = int(request.GET.get(arg, 1))
#         arg = get_condition(arg)
#     except:
#         arg = 1


@require_POST1
def reg(request: HttpRequest):
    print(request.POST)

    print(request.GET)
    print(request.body)
    try:
        payload = simplejson.loads(request.body)
        print(type(payload), payload)
        username = payload['username']

        count = User.objects.filter(username=username).counter()
        if count:
            return JsonResponse(Messages.USER_EXISTS)

        email = payload['email']
        password = payload['password']
        print(username, email, password)
        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({}, status=201)

    except Exception as e:  # 有任何异常，都返回
        print(e)
        # Json错误信息
        return JsonResponse(Messages.BAD_REQUEST)

# 实现用户登录后才可以访问：
# 1. @login_required装饰器
# 2. 中间件技术
# 3. 自定义装饰器
# @login_required装饰器，但是它会在服务器端重定向。
# 如果采用是前后端分离，需要后端返回状态值，有前端路由实现跳转。
# 所以此装饰器不适合。


# # 中间件Middleware
# # 官方定义：在Django的request和response处理过程中，由框架提供的钩子（hook）。
# # 用途：因为中间件可以拦截所有视图函数，所以当需要拦截大部分请求和响应时，
# # 用中间件比较合适，一般用在例如浏览器端的IP是否禁用、UserAgent分析、异常响应的统一处理等。
# # 对于只拦截部分请求的情况，可以使用装饰器
#
# # 中间件的工作原理：
# # 中间件可以通过类实现也可以通过函数实现，大部分都可以通过类来实现
# # 以类实现方式为例：
# # Django中间件使用的洋葱式解析顺序
# # 在call方法中会调用，self.get_response()，在self.get_response
# # 之前的代码，会根据settings中的顺序先后执行，全部执行完解析路径映射到view_func，
# # 然后再根据setting中的顺序，先后执行process_view()内部代码，
# # process_view()方法，在视图函数执行之前被调用，
# # 它可以返回None，也可以返回HTTPResponse对象，
# # 如果返回None，会继续执行请求，如果返回response对象，此函数返回值作为浏览器端的响应，
# # 而且后面的process_view（）及视图函数将不会被调用。
# # 当所有的process_view（）函数都返回None时，会执行view函数
# # 然后逆序执行所用中间件中的，self.get_response()后面的代码。
# # 需要注意的是：get_response(request)之前代码中，如果存在return HttpResponse()，
# # 将从当前中间件立即返回给浏览器，从洋葱中依次反弹
#
#
#
#
#
#
#
# class SimpleMiddleware1:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.
#
#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         print(1, '-' * 30)
#         print(isinstance(request, HttpRequest))
#         print(request.GET)
#         print(request.POST)
#         print(request.body)
#         # 之前相当于老版本的process_request #return HttpResponse(b'', status=404)
#         response = self.get_response(request)
#         # Code to be executed for each request/response after
#         # the view is called.
#         print(101, '-' * 30)
#         return response
#
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         print(2, '-' * 30)
#         print(view_func.__name__, view_args, view_kwargs)
#         # 观察view_func名字，说明在process_request之后，process_view之前已经做好了路径映射
#         return None  # 继续执行其它的process_view或view
#         # return HttpResponse('111', status=201)
#
#
# class SimpleMiddleware2:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.
#
#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         print(3, '-' * 30)
#         # return HttpResponse(b'', status=404)
#         response = self.get_response(request)
#
#         # Code to be executed for each request/response after
#         # the view is called.
#         print(102, '-' * 30)
#         return response
#
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         print(4, '-' * 30)
#
#         print(view_func.__name__, view_args, view_kwargs)
#         # return None # 继续执行其它的process_view或view
#         return HttpResponse('2222', status=201)
#
#
# # 运行结果：
# # 1 ------------------------------
# # True
# # <QueryDict: {}>
# # <QueryDict: {}>
# # b''
# # 3 ------------------------------
# # 2 ------------------------------
# # test () {}
# # 4 ------------------------------
# # test () {}
# # "GET /users/test HTTP/1.1" 201 4
# # 因为SimpleMiddleware1的process_view return None
