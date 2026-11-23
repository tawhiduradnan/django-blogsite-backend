from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostCreateForm , CommentForm
from posts.models import Category, Comment, Post


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
    parent_comments = post.comments.filter(parent__isnull=True).select_related('author')
    comment_form = CommentForm()
    reply_form = CommentForm()
    comment_form.fields['body'].widget.attrs.update(
        {'placeholder': 'Write a comment...'}
    )
    reply_form.fields['body'].widget.attrs.update(
        {'rows': 1, 'placeholder': 'Reply...'}
    )
    reply_parent_id = ''
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        reply_parent_id = request.POST.get('parent_id', '')
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            if reply_parent_id:
                # Replies must belong to this post; never attach a comment to
                # an unrelated post based on an arbitrary submitted ID.
                comment.parent = get_object_or_404(
                    post.comments, pk=reply_parent_id
                )
            comment.save()
            return redirect('posts:post_detail', pk=post.pk)
        if reply_parent_id:
            reply_form = form
            reply_form.fields['body'].widget.attrs.update(
                {'rows': 1, 'placeholder': 'Reply...'}
            )
        else:
            comment_form = form
            comment_form.fields['body'].widget.attrs.update(
                {'placeholder': 'Write a comment...'}
            )

    return render(
        request,
        'post_detail.html',
        {
            'post': post,
            'comments': parent_comments,
            'comment_form': comment_form,
            'reply_form': reply_form,
            'reply_parent_id': reply_parent_id,
        },
    )



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
