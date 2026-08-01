from django.shortcuts import render

from .models import Author, Book, BookInstance

from django.views import generic

# Create your views here.

"""
收到请求
   ↓
找到 index.html
   ↓
把它渲染成 HTTP 响应
   ↓
返回浏览器
"""
def index(request): # index view?

    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(
        status="a"
    ).count()

    num_authors = Author.objects.count()

    context = {
        "num_books" : num_books,
        "num_instances" : num_instances,
        "num_instances_available" : num_instances_available,
        "num_authors" : num_authors,
    }

    return render(request, "index.html", context)    # 什么是render 什么是view？
    # 根据请求渲染 index.html吗？ request 是浏览器请求进入 Django 后形成的对象
    # 所以啥是view函数啊

class BookListView(generic.ListView):  # 怎么这个View就是个类了
    model = Book
    paginate_by = 10
   # 自动查询所有book，将结果命名为book_list，加载book_list.html

class BookDetailView(generic.DetailView):
    model = Book 
   # 自动读取URL中的pk，查询对应Book，将对象命名为book，加载catalog/book_detail.html

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
