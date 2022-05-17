from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone



# python manage.py makemigrations -- [sql] كا مترجم يتم تحويل قاعدة البيانات من بايثون الي
# python manage.py migrate        -- [sql] أنشاء جدول


# جدول التدوينات
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        # return '/detail/{}'.format(self.pk)
        return reverse('detail', args=[self.pk])


    # post_date كلاس يتم فية الية الترتيب عن طريق
    # post_date من الاقدم الي الاحدث
    # -post_date من الاحدث الي الاقدم
    class Meta:
        ordering = ('-post_date', )


class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name='الاسم')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    body = models.TextField(verbose_name='التعليق')
    comment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    # علاقة بين جدول التعليقات و جدول البيانات
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return 'علق {} على {}.'.format(self.name, self.post)
    
    class Meta:
        ordering = ('-comment_date', )
