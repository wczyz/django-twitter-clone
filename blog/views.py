from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from el_pagination.views import AjaxListView
from .models import Post, Star


class PostListView(AjaxListView):
    model = Post
    template_name = 'blog/home.html'
    page_template = 'blog/home_page.html'
    context_object_name = 'posts'


class UserPostListView(AjaxListView):
    model = Post
    template_name = 'blog/user_profile.html'
    page_template = 'blog/user_posts_page.html'
    context_object_name = 'posts'

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.get_user()
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posting_user'] = self.get_user()
        return context


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def star(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        starred_post = Post.objects.get(id=post_id)
        m = Star(post=starred_post)
        m.save()
        return HttpResponse('success')
    else:
        return HttpResponse('unsuccesful')
