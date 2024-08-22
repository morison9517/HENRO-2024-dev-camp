from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

def index(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # request.FILESを追加
        if form.is_valid():
            form.save()
            return redirect('comp')
    else:
        form = PostForm()
    
    return render(request, 'nikki/index.html', {'form': form})

def comp(request):
    posts = Post.objects.all().order_by('-created_at')  # 投稿日時で逆順に並べる

    params = {
       'data' : posts
    }
    return render(request, "nikki/comp.html", params)
