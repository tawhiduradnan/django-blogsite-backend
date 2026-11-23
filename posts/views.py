from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostCreateForm
from posts.models import Category, Post


def post_list_view(request):
    query = request.GET.get('query', '').strip()
    category_id = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()

    posts = Post.objects.select_related('category', 'author')
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(author__username__icontains=query)
            | Q(category__category_name__icontains=query)
        )
    if category_id:
        posts = posts.filter(category_id=category_id)
    valid_statuses = {value for value, _label in Post.STATUS_CHOICES}
    if status in valid_statuses:
        posts = posts.filter(status=status)

    categories = Category.objects.annotate(post_count=Count('posts'))
    total_posts = (
        Post.objects.filter(author=request.user).count()
        if request.user.is_authenticated
        else 0
    )

    return render(
        request,
        'post_list.html',
        {
            'posts_summary': posts,
            'total_posts': total_posts,
            'my_categories': categories,
            'categories': categories,
            'status_choices': Post.STATUS_CHOICES,
            'query': query,
            'selected_category': category_id,
            'selected_status': status,
        },
    )


def post_detail_view(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('category', 'author'), pk=pk
    )
    return render(request, 'post_detail.html', {'post': post})


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostCreateForm()

    return render(request, 'post_creation.html', {'form': form})
