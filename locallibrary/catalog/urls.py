from django.urls import path
from catalog import views

"""
/catalog/
    ↓ 总路由吃掉 catalog/
剩余 ""
    ↓
path("", views.index)
    ↓
调用 views.index(request)
"""

urlpatterns = [
    path('', views.index, name='index'),    # name 只是给这条 URL 起了一个内部名字。
]