from django.db import models
from django.urls import reverse  # 用于通过反转URL模式生成URL
import uuid # 单一图书实例要求
from django.contrib.auth.models import User
from datetime import date

class Language(models.Model):
    """代表一种语言的模型（例如英语、法语、日语等）"""
    name = models.CharField(max_length=200,
                            help_text="输入这本书的语言 (例如： 英语, 法语, 中文 等。)")

    def __str__(self):
        """表示模型对象的字符串（在管理站点中）"""
        return self.name

class Genre(models.Model):
    """
    这个模型用于存储关于书籍类别的信息。例如是否是小说或非小说，浪漫史或军事历史等。
    """
    name=models.CharField(max_length=200,help_text="输入书的体裁(例如：科幻小说, 法国诗歌。)")

    def __str__(self):
        """
        表示模型对象的字符串（在管理站点中）
        """
        return self.name


class Book(models.Model):
    """
    这个模型用于存储关于书籍的详细信息。
    """
    title = models.CharField(max_length=200)    #书名
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # 使用了外键，因为书籍只能有一个作者，但作者可以有多本书
    # 将其作为字符串而不是对象进行编写，因为文件中尚未声明它。
    summary = models.TextField(max_length=1000, help_text="输入对这本书的简要描述")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13个字符 <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="为这本书选择一个体裁")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    # 使用manytomanyfield是因为类型可以包含许多书。书籍可以涵盖多种体裁。
    # 体裁类已经定义，因此我们可以指定上面的对象。

    def __str__(self):
        """
        用于表示模型对象的字符串。
        """
        return self.title

    def get_absolute_url(self):
        """
        返回访问特定图书实例的URL。
        """
        return reverse('book-detail', args=[str(self.id)])  #args=[str(self.id)]用法不了解

    def display_genre(self):
        """
        为流派创建字符串。这是在“管理”中显示流派所必需的。
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    该 BookInstance 代表一本书，有人可能借用的一个特定副本，包括有关副本是否可用在什么日期预计还，“印记“或版本的详细信息，并为这本书在图书馆给予一个唯一的ID信息。
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="整个图书馆中此特定图书的唯一ID")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    #借阅者
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', '维护'),
        ('o', '在借'),
        ('a', '可用'),
        ('r', '已还'),
    )

    # 查看当前借阅情况是否过期
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='图书可用性')

    class Meta:
        '''
        模型的元数据，指的是“除了字段外的所有内容”，例如排序方式、数据库表名、人类可读的单数或者复数名等等。
        '''
        ordering = ["due_back"]   #按照归还日期排序
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        用于表示模型对象的字符串。
        """
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    """
    该模型将作者定义为具有名字，姓氏，出生日期和（可选）死亡日期。
    """
    first_name = models.CharField(max_length=100)     #名
    last_name = models.CharField(max_length=100)      #姓
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        返回访问特定作者实例的URL。
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        用于表示模型对象的字符串。
        """
        return '%s, %s' % (self.last_name, self.first_name)


