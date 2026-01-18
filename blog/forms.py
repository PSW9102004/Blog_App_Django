from django import forms
from .models import Comment, Post  # <--- 'Tag' is removed

class PostForm(forms.ModelForm):
    # We can keep this field definition to make the UI look nice (placeholder, help text)
    # django-taggit expects a simple text string, which this provides.
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags (e.g. design, startup, ai).',
        widget=forms.TextInput(attrs={'placeholder': 'design, startup, ai'})
    )

    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'content', 'status', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
