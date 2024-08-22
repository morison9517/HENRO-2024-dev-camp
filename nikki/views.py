from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  # データベースに保存
            return redirect('index')  # 保存後にリダイレクト
    else:
        form = PostForm()

    posts = Post.objects.all()  # データベースから全ての投稿を取得
    return render(request, 'nikki/index.html', {'form': form, 'posts': posts})

def comp(request):
    return render(request, "nikki/comp.html",{
        "comp":"comp"
    })
