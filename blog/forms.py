from django import forms
from django.utils.text import slugify
from .models import Comment, Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags (e.g. design, startup, ai).',
        widget=forms.TextInput(attrs={'placeholder': 'design, startup, ai'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(
                self.instance.tags.values_list('name', flat=True)
            )

    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'content', 'status', 'tags']

    def clean_tags(self):
        raw_tags = self.cleaned_data.get('tags', '')
        tags = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]
        return tags

    def save(self, commit=True):
        post = super().save(commit=commit)
        if commit:
            tags = self.cleaned_data.get('tags', [])
            tag_objects = []
            for tag in tags:
                slug = slugify(tag)[:50] or tag.lower().replace(' ', '-')
                tag_obj, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': tag})
                if tag_obj.name != tag:
                    tag_obj.name = tag
                    tag_obj.save(update_fields=['name'])
                tag_objects.append(tag_obj)
            post.tags.set(tag_objects)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
