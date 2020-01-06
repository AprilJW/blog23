from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.transaction import atomic

class PostView(View):
    def get(self, request: HttpRequest):
        print('get request', request)
        return JsonResponse({'method': 'get'})

    def post(self, request: HttpRequest):
        print('post request', request)
        return JsonResponse({'method': 'post'})


def getpost(request: HttpRequest, id):
    print(type(id), id)
    return JsonResponse({})
