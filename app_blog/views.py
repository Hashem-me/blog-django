from django.shortcuts import render, get_object_or_404, redirect
from django.template import context
from app_blog.models import Post, Comment
from .forms import NewComment
# Create your views here.


def home(request):
    context = {
        'title': 'الصفحة الرئيسية',
        'posts': Post.objects.all(),
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
