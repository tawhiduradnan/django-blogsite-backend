from django.forms import ModelForm
from posts.models import Post, Comment
class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']