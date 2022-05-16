from django import forms
from django.shortcuts import redirect, render

from app_blog.models import Post
from .forms import LoginForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            # messages.success(
            #    request, 'تهانينا {} لقد تمت عملية التسجيل بنجاح.'.format(username))
            messages.success(
                request, f'تهانينا {username} لقد تمت عملية التسجيل بنجاح.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app_user/register.html', {
        'title': 'التسجيل',
        'form': form,
    })


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(
                request, 'هناك خطأ في اسم المستخدم أو كلمة المرور.')

    return render(request, 'app_user/login.html', {
        'title': 'تسجيل الدخول',
    })


def logout_user(request):
    logout(request)
    return render(request, 'app_user/logout.html', {
        'title': 'تسجيل الخروج'
    })
    
    


# @login_required(login_url='login')
def profile(request):
    posts = Post.objects.filter(author=request.user)
    post_list = Post.objects.filter(author=request.user)
    # paginator = Paginator(post_list, 10)
    # page = request.GET.get('page')
    # try:
    #     post_list = paginator.page(page)
    # except PageNotAnInteger:
    #     post_list = paginator.page(1)
    # except EmptyPage:
    #     post_list = paginator.page(paginator.num_page)
    return render(request, 'app_user/profile.html', {
        'title': 'الملف الشخصي',
        'posts': posts,
        # 'page': page,
        # 'post_list': post_list,
    })

