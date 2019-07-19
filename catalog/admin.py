from django.contrib import admin
from .models import Author, Genre, Book, BookInstance,Language
#admin.site.register(Book)
#admin.site.register(Author)
# 定义管理类
class BookInline(admin.TabularInline):
    model = Book
    extra=0 #去掉多余的显示
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

# 用关联的模型注册管理类
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(BookInstance)
# 使用decorator(装饰器)为Book注册管理类
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra=0 #去掉多余的显示

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre','language')
    inlines = [BooksInstanceInline]
# 使用decorator为BookInstance注册管理类

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status','borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Details', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

# Register your models here.
