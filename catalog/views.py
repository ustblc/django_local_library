from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

def index(request):
    """
    网站主页的查看功能。
    """
    #访问此视图的次数（在会话变量中计数）。
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # 生成一些主要对象的计数
    num_books=Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # 可用书籍（状态为“a”）
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # 默认情况下，“all（）”是隐含的。

    # 使用上下文变量中的数据呈现html template index.html
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,'num_visits':num_visits},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2   #分页显示
class BookDetailView(generic.DetailView):
    model = Book
# Create your views here.
class AuthorListView(generic.ListView):
    model =  Author
    paginate_by = 1   #分页显示
class AuthorDetailView(generic.DetailView):
    model =  Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    基于类的通用视图，列出借给当前用户的图书。
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """基于类的通用视图，列出所有出借图书。只有具有can_mark_返回权限的用户才可见。"""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # 如果这是一个POST请求，则处理表单数据
    if request.method == 'POST':

        # 创建一个表单实例并用来自请求的数据填充它（绑定）：
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # 按要求处理form.cleaned_数据（这里我们只需将其写入model due_back字段）
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # 如果这是GET（或任何其他方法），请创建默认表单。
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(PermissionRequiredMixin,CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'

class BookCreate(PermissionRequiredMixin,CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin,UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'
