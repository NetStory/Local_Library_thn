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

    path(
        'books/',
        views.BookListView.as_view(),   # 这是什么鬼
        name='books',
    ),

    path(
        'book/<int:pk>',    # pk又是啥 将整数命名为pk，传给BookDetailView
        views.BookDetailView.as_view(),
        name='book-detail',
    ),

    path(
        'authors/',
        views.AuthorListView.as_view(),
        name='authors',
    ),

    path(
        'author/<int:pk>',
        views.AuthorDetailView.as_view(),
        name='author-detail',
    )
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserList.as_view(), name='my-borrowed'),
]