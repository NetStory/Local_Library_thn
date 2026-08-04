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

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')   # 这是啥
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """

    book_inst = get_object_or_404(BookInstance, pk=pk)  # 尼玛这个BookInstance是个类名吗

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # 创建一个form实例，用request中POST过来的data绑定填充
        form = RenewBookForm(request.POST)

        # 检查表单是否合法
        if form.is_valid():
            # 用cleaned_data吧数据拿出来，给实例写入信息
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save() # 更新信息

            return HttpResponseRedirect(reverse('my-borrowed')) 

    else:   # 如果这是个GET请求（来请求获得default form）
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={
            'renewal_date' : proposed_renewal_date,
        })           

    return render(request, 
                  'catalog/book_renew_librarian.html', 
                  {'form' : form, 'bookinst': book_inst}
                  )

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"


class AuthorUpdate(UpdateView):
    model = Author
    fields = [
        "first_name",
        "last_name",
        "date_of_birth",
        "date_of_death",
    ]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("authors")