import uuid  # 给每一本实体副本生成唯一编号

from django.db import models
from django.urls import reverse  # 根据 URL 配置中的名字，反向生成具体 URL


# Create your models here.


# 体裁
class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre"
    )

    def __str__(self):
        return self.name


# 书
class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey(
        "Author",
        # 这里 "Author" 写成字符串，是因为 Author 类还没有在文件中定义。
        # Python 执行到这里时还不认识 Author 类，因此让 Django 稍后再寻找它。

        on_delete=models.SET_NULL,
        # 当外键对应的作者被删除时，不删除这本书，
        # 而是把这本书的 author 字段设置为 NULL。

        null=True
        # 数据库允许 author 这一列保存 NULL。
        # 这也是 SET_NULL 能够工作的前提。
    )

    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book"
    )

    isbn = models.CharField(
        "ISBN",
        # 这是 verbose_name，也就是这个字段展示给人看的名字。
        # 如果不写，Django 会根据变量名 isbn 自动显示成 "Isbn"。
        # 这里希望按照标准写法显示为全大写 "ISBN"。

        max_length=13,
        help_text="13 Character ISBN number"
    )

    genre = models.ManyToManyField(
        # 这个是什么 Field？
        # ManyToManyField 表示“多对多关系”。
        #
        # 一本书可以属于多个体裁：
        # 《三体》可以同时属于科幻、中国文学。
        #
        # 一个体裁也可以拥有很多本书：
        # 科幻体裁可以包含《三体》《沙丘》等。
        #
        # Django 会在数据库里自动创建一张中间关系表，
        # 专门记录哪些 Book 和哪些 Genre 相连。

        Genre,
        # 这他妈怎么直接一个类就蹦出来了？
        #
        # ManyToManyField 的第一个参数，需要告诉 Django：
        # “我要和哪一种模型建立关系？”
        #
        # Genre 类已经在上面定义过了，因此这里可以直接传入 Genre 类本身。
        #
        # 可以把它理解成：
        # genre 指向的不是一个普通字符串，而是一批 Genre 对象。
        #
        # 这里写 Genre 或者写字符串 "Genre" 都可以：
        # Genre      -> Python 当前已经认识这个类
        # "Genre"    -> Django 稍后再根据名字寻找这个类

        help_text="Select a genre for this book"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # 这他妈又是在干啥？
        #
        # 这个方法的任务是：
        # 返回“当前这本书的详情页面地址”。
        #
        # 例如当前书的 id 是 7，
        # 最终可能生成：
        #
        # /catalog/book/7/
        #
        # 它现在不会自己显示网页，
        # 只是告诉 Django：
        # “要访问这个 Book 对象，应该去哪个 URL。”

        return reverse(
            "book-detail",
            # reverse 不直接手写 "/catalog/book/7/"，
            # 而是去 urls.py 中寻找 name="book-detail" 的 URL 规则。

            args=[str(self.id)]
            # 这 id 他妈哪里来的？
            #
            # Book 模型没有手动声明主键，
            # 所以 Django 会自动添加一个自增主键，大致相当于：
            #
            # id = models.BigAutoField(primary_key=True)
            #
            # 第一条 Book 记录的 id 可能是 1，
            # 第二条可能是 2，以此类推。
            #
            # 假设 self.id == 7，
            # reverse 会把 7 填进 book-detail 对应的 URL 规则里。
        )

    def display_genre(self):    # 这他妈啥机制啊
        """
        Creates a string for the genre, This is required to display genre in Admin
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'   # 这又是在干啥

class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,

        default=uuid.uuid4,
        # 这什么鬼？
        #
        # uuid.uuid4 是一个用于生成随机 UUID 的函数。
        #
        # UUID 大致长这样：
        # 550e8400-e29b-41d4-a716-446655440000
        #
        # 每创建一个新的 BookInstance，
        # Django 都会调用一次 uuid.uuid4，
        # 给这一本实体副本生成一个几乎不会重复的编号。
        #
        # 注意这里不能写成 uuid.uuid4()。
        #
        # uuid.uuid4   -> 把函数交给 Django，每次创建对象时再调用
        # uuid.uuid4() -> 现在立刻调用一次，容易把同一个结果当默认值

        help_text="Unique ID for this particular book"
    )

    book = models.ForeignKey(
        "Book",
        # 为毛这里又变成字符串了，前面 Book 已经定义了啊？
        #
        # 这里确实不必写成字符串。
        # 因为 Book 已经在上面定义过，所以完全可以写：
        #
        # book = models.ForeignKey(
        #     Book,
        #     ...
        # )
        #
        # 但是写成 "Book" 也完全合法。
        # 字符串属于 Django 的“延迟模型引用”写法：
        # Django 在所有模型加载完成后，再根据名字寻找 Book。
        #
        # 教程这里保持字符串写法，主要是为了写法统一，
        # 不是因为必须写字符串。

        on_delete=models.SET_NULL,
        null=True
    )

    imprint = models.CharField(max_length=200)
    # 这是啥？
    #
    # imprint 在图书领域表示这一本实体书的出版版本或出版信息。
    # 可以粗略理解成：
    #
    # “这本实体副本是哪一个出版社、哪一个版本印出来的？”
    #
    # 例如：
    # "Penguin Books, 2020 edition"
    # "重庆出版社，2008 年版"
    #
    # 它描述的是这一实体副本的版本信息，
    # 不是整本书的标题。

    due_back = models.DateField(
        null=True,

        blank=True
        # 这是在干啥？
        #
        # blank=True 表示：
        # 在 Django 表单或者后台管理页面中，
        # 这个字段允许用户不填写。
        #
        # null=True 表示：
        # 数据库里面允许保存 NULL。
        #
        # 可以记成：
        #
        # blank 管“用户输入时能不能留空”
        # null  管“数据库里能不能没有值”
        #
        # 一本当前可借的书没有归还日期，
        # 所以 due_back 合理地允许为空。
    )

    LOAN_STATUS = (
        # 这是个啥，元组套元组？
        #
        # 对，这是一个“选项表”。
        #
        # 外层元组装着所有可选状态；
        # 每个内层元组表示一个选项：
        #
        # (数据库实际保存的值, 展示给用户看的文字)

        ("m", "Maintenance"),
        # 数据库存 "m"，页面显示 "Maintenance"

        ("o", "On loan"),
        # 数据库存 "o"，页面显示 "On loan"

        ("a", "Available"),
        # 数据库存 "a"，页面显示 "Available"

        ("r", "Reserved"),
        # 数据库存 "r"，页面显示 "Reserved"
    )

    status = models.CharField(
        max_length=1,
        # 因为实际保存的只有 m、o、a、r，所以长度 1 就够了。

        choices=LOAN_STATUS,
        # 告诉 Django：
        # status 只能从 LOAN_STATUS 定义的选项中选择。
        #
        # Django 后台中会自动显示成下拉菜单，
        # 而不是让用户随便输入字符串。

        blank=True,
        # 表单中允许不填写。
        # 不过这里又提供了 default="m"，
        # 所以不填时通常会使用默认值 m。

        default="m",
        # 新建实体副本时，默认状态是 Maintenance。

        help_text="Book availability"
    )

    class Meta:
        ordering = ["due_back"]
        # 这是干啥用的？
        #
        # Meta 用于设置“整个模型的管理规则”。
        #
        # ordering = ["due_back"] 表示：
        # 查询 BookInstance 时，默认按照归还日期从早到晚排序。
        #
        # 例如：
        # 8 月 1 日
        # 8 月 5 日
        # 8 月 20 日
        #
        # 如果写成：
        # ordering = ["-due_back"]
        #
        # 前面的负号表示倒序，也就是从晚到早。

    def __str__(self):
        return f"{self.id} ({self.book.title})"
        # 这里的 id 又尼玛是啥啊？
        #
        # 这里的 id 就是本模型最上面手动定义的 UUIDField：
        #
        # id = models.UUIDField(...)
        #
        # 它和 Book 中 Django 自动创建的整数 id 不一样。
        #
        # Book.id：
        # 1、2、3、4……
        #
        # BookInstance.id：
        # 550e8400-e29b-41d4-a716-446655440000
        #
        # 最终这个对象显示出来可能是：
        #
        # 550e8400-e29b-41d4-a716-446655440000 (The Three-Body Problem)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    date_of_death = models.DateField(
        "Died",
        # 这他妈怎么又来一个字符串，用来干啥的？
        #
        # "Died" 是这个字段的 verbose_name，
        # 也就是展示给用户看的字段名称。
        #
        # Python 变量名仍然是：
        # date_of_death
        #
        # 但是 Django 后台或表单中显示：
        # Died
        #
        # 它不是默认值，也不是数据库中保存的内容，
        # 只是一个更适合人阅读的标签。

        # 那为啥 date_of_birth 没有？
        #
        # 因为不写 verbose_name 时，
        # Django 会自动根据变量名生成标签。
        #
        # date_of_birth
        # 会自动变成：
        # Date of birth
        #
        # 作者觉得这个自动名称已经足够清楚，
        # 所以没有额外指定。
        #
        # date_of_death 本来也会自动显示成：
        # Date of death
        #
        # 这里只是特意把它缩短成：
        # Died

        null=True,
        blank=True
    )

    def get_absolute_url(self):
        # 和 Book 的 get_absolute_url 完全是同一个机制：
        # 返回当前 Author 对象的详情页 URL。

        return reverse(
            "author-detail",
            # reverse 到底是在干啥？
            #
            # reverse 会去 urls.py 中寻找：
            #
            # name="author-detail"
            #
            # 的 URL 规则，然后把参数填进去。
            #
            # 假设 urls.py 中有：
            #
            # path(
            #     "author/<int:pk>/",
            #     views.AuthorDetailView.as_view(),
            #     name="author-detail"
            # )
            #
            # 当前作者 self.id == 3，
            # 那么 reverse 最终会生成：
            #
            # /catalog/author/3/
            #
            # 它的核心意义是：
            # 不要把 URL 地址硬编码在模型里。
            #
            # 以后即使 URL 路径改了，
            # 只要 name="author-detail" 没变，
            # 这里的代码就不用改。

            args=[str(self.id)]
            # Author 也没有手动定义主键，
            # 所以 Django 自动为它添加整数 id。
            #
            # 这里把当前作者的 id 作为 URL 参数传给 reverse。
        )

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"