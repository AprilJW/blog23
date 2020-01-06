from django.urls import path
from.views import userlogin, reg

urlpatterns = [
    path('login', userlogin),
    path('', reg)

]