from django.shortcuts import render

from .models import Author, Book, BookInstance

from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
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

    # 如果当前session没有这个字段，把这个信息加入session？
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    context = {
        "num_books" : num_books,
        "num_instances" : num_instances,
        "num_instances_available" : num_instances_available,
        "num_authors" : num_authors,
        'num_visits' : num_visits
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

class LoanedBooksByUserList(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by=10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')