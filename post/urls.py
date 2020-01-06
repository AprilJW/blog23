from django.urls import path
from.views import getpost, PostView

urlpatterns = [
    path('', PostView.as_view()),  # 将类包装成函数，可以包装多个函数
    path('<int:id>', getpost),

]