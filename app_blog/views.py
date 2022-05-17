from django.shortcuts import render, get_object_or_404, redirect
from django.template import context
from app_blog.models import Post, Comment
from .forms import NewComment, PostCreateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 4) # اظهار عدد التدوينات
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'title': 'الصفحة الرئيسية',
        'posts': posts,
        'page' : page,
    }
    return render(request, 'app_blog/index.html', context)

# من نحن


def about(request):
    return render(request, 'app_blog/about.html', {'title': 'من نحن'})

# تفاصيل المدونة


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(active=True)

    # check before save data from comment form
    if request.method == 'POST':
        comment_form = NewComment(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = NewComment()
            # return redirect('detail', post_id)
    else:
        comment_form = NewComment()

    context = {
        'title': post,
        'post':  post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'app_blog/detail.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content']
    template_name = 'app_blog/new_post.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'app_blog/post_update.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # دالة اختبار او تحقق 
    # هل المستخم الذي انا مسجل فية هل هو صاحب التدوينة الذي يتم التعديل عليها
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
