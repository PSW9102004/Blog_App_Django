from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse
from taggit.models import Tag # <--- CHANGED: Import from taggit, not .models
from .models import Post
from .forms import CommentForm, PostForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_queryset(self):
        return (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .select_related('author', 'author__profile')
            .prefetch_related('tags', 'likes')
            .order_by('-date_posted')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Discover stories, thinking, and expertise'
        context['page_description'] = 'Read, write, and connect with writers on any topic.'
        return context

class PostDetailView(DetailView):
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Allow authors to see their own drafts
        if self.request.user.is_authenticated:
            return (
                Post.objects.filter(
                    models.Q(status=Post.Status.PUBLISHED) | models.Q(author=self.request.user)
                )
                .select_related('author', 'author__profile')
                .prefetch_related('tags', 'likes', 'bookmarks', 'comments', 'comments__author')
                .distinct()
            )
        # Everyone else only sees published posts
        return (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .select_related('author', 'author__profile')
            .prefetch_related('tags', 'likes', 'bookmarks', 'comments', 'comments__author')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_liked'] = self.object.likes.filter(pk=self.request.user.pk).exists()
            context['has_bookmarked'] = self.object.bookmarks.filter(pk=self.request.user.pk).exists()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

class TagPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        # We find the Tag object from taggit
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return (
            Post.objects.filter(tags=self.tag, status=Post.Status.PUBLISHED)
            .select_related('author', 'author__profile')
            .prefetch_related('tags', 'likes')
            .order_by('-date_posted')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Tag: {self.tag.name}'
        context['page_description'] = f'Browse stories tagged with "{self.tag.name}".'
        return context

class BookmarkListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return (
            self.request.user.bookmarked_posts.filter(status=Post.Status.PUBLISHED)
            .select_related('author', 'author__profile')
            .prefetch_related('tags', 'likes')
            .order_by('-date_posted')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Your bookmarks'
        context['page_description'] = 'Quickly pick up stories you saved for later.'
        return context

@login_required
@require_POST
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.POST.get('next') or reverse('post-detail', kwargs={'slug': slug}))

@login_required
@require_POST
def toggle_bookmark(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.bookmarks.filter(pk=request.user.pk).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return redirect(request.POST.get('next') or reverse('post-detail', kwargs={'slug': slug}))
