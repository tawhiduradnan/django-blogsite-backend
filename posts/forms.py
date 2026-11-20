from django.forms import ModelForm
from posts.models import Post, Comment
class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']