from django.shortcuts import render
from posts.models import Post
from django.contrib.auth.decorators import login_required
from posts.forms import PostCreateForm
# Create your views here.
def post_list_view(request):
    try:
        posts = Post.objects.all()
        post_summary_list = []
        for post in posts:
            post_summary_list.append(
                {'id': post.id, 'title': post.title, 'content': post.content[:100], 'category': post.category.category_name if post.category else None, 'status': post.status, 'author': post.author.username if post.author else None}
            )
    except Exception as e:
        print(f"Error occurred: {e}")
    return render(request=request, template_name='post_list.html', context={'posts_summary':post_summary_list})
    

def post_detail_view(request, pk):
    try:
        post = Post.objects.get(id=pk)
        return render(request=request, template_name='post_detail.html', context={'post': post})
    except Exception as e:
        return render(request=request, template_name='post_not_found.html', context={'error': e})

@login_required
def post_create_view(request):
    try:
        form = PostCreateForm()
        if request.method == 'POST':
            form = PostCreateForm(request.POST)
            if form.is_valid():
                post=Post(
                    title=request.POST.get('title'),
                    content=request.POST.get('content'),
                    category_id=request.POST.get('category'),
                    author=request.user
                )
                post.save()
        return render(request=request, template_name='post_creation.html', context={'form': form})
    except Exception as e:
        return render(request=request, template_name='post_creation.html', context={'error': e}) 