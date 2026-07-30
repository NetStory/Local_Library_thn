from django.contrib import admin

# Register your models here. 为啥要注册啊 不注册会咋样啊
from .models import Author, Genre, Book, BookInstance

#admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)

# 管理特定model的管理员? 这他妈是在干啥 还是只是Admin在Author这一页会看到的东西？
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')] # 元组则会水平展示
admin.site.register(Author, AuthorAdmin)


# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    # 剖切细节视图, 让页面更美观
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

class BooksInstanceInline(admin.TabularInline): # 水平布局
    model = BookInstance    # 这是在干啥？Inline信息？

# Register the Admin classes for Book using the decorator
@admin.register(Book) # @register 装饰器来注册模型（这和 admin.site.register() 
class BookAdmin(admin.ModelAdmin):  # 这他妈到底是在干啥啊
    list_display = ('title', 'author', 'display_genre') # 所以这里穿的是一个函数？那他妈鬼才知道这是个函数啊 这不是个字符串吗   
    inlines = [BooksInstanceInline] # 把书籍信息和其实例信息一起展示
