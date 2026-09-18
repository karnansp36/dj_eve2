from django.shortcuts import render, redirect
from .forms import User_postForm
# Create your views here.
from .models import User_post
def user_post(request):
    if request.method == 'POST':
        form = User_postForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'user_post.html', {'form': User_postForm(), 'success': True})

    return render(request, 'user_post.html', {'form': User_postForm()})


def profile_views(request):
    posts = User_post.objects.all()
    return render(request, 'profile.html', {'posts': posts})

def profile_data(request, id):
    post = User_post.objects.get(id=id)
    return render(request, 'profile_data.html', {'post': post})


def profile_edit(request, id):
    post = User_post.objects.get(id=id)
    if request.method == 'POST':
        form = User_postForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile_views')
    else:
        form = User_postForm(instance=post)
    return render(request, 'profile_edit.html', {'form': form})