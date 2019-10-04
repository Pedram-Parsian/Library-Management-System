from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import forms
from . import models


class BlogHomeView(ListView):
    model = models.Post
    template_name = 'blog/home.html'
    paginate_by = 3
    ordering = ['-date_published']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.PostCategory.objects.all()
        context['tags'] = models.PostTag.get_all_with_size()
        context['archives'] = models.Post.get_archives()
        context['popular_posts'] = models.Post.get_popular_posts()
        context['navbar'] = 'blog'
        return context


# BUG: should be like https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#an-alternative-better-solution
class BlogDetailView(FormMixin, DetailView):
    template_name = 'blog/detail.html'
    model = models.Post

    def get_form_class(self):
        return forms.LogedInUser_CommentForm if self.request.user.is_authenticated else forms.AnonymousUser_CommentForm

    def get_success_url(self):
        return reverse('blog:post', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.PostCategory.objects.all()
        context['tags'] = models.PostTag.get_all_with_size()
        context['comments'] = models.PostComment.objects.filter(post=self.get_object(), status=models.PostComment.APPROVED)
        context['archives'] = models.Post.get_archives()
        context['popular_posts'] = models.Post.get_popular_posts()
        context['related_posts'] = self.get_object().get_related_posts()
        context['form'] = self.get_form()
        context['navbar'] = 'blog'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = models.PostComment(post=self.get_object())
        if self.request.user.is_authenticated:
            comment.user = self.request.user
        else:
            comment.name = form.cleaned_data.get('name')
            comment.email = form.cleaned_data.get('email')
        comment.text = form.cleaned_data.get('text')
        comment.save()
        messages.success(self.request, "Your comment has been submitted. It will show up when it's approved!")
        return super(BlogDetailView, self).form_valid(form)


class BlogArchiveView(ListView):
    model = models.Post
    template_name = 'blog/home.html'
    paginate_by = 5

    def get_queryset(self):
        return models.Post.objects.get_archive(self.kwargs['year'], self.kwargs['month'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.PostCategory.objects.all()
        context['tags'] = models.PostTag.get_all_with_size()
        context['archives'] = models.Post.get_archives()
        context['popular_posts'] = models.Post.get_popular_posts()
        selected_year = self.kwargs['year']
        selected_month = self.kwargs['month']
        context['title'] = f'Posts from {selected_year}/{selected_month}'
        context['navbar'] = 'blog'
        return context


class BlogTagView(ListView):
    model = models.Post
    template_name = 'blog/home.html'
    paginate_by = 5

    def get_queryset(self):
        return models.PostTag.objects.get(slug=self.kwargs['tag']).post_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.PostCategory.objects.all()
        context['tags'] = models.PostTag.get_all_with_size()
        context['archives'] = models.Post.get_archives()
        context['popular_posts'] = models.Post.get_popular_posts()
        selected_tag_title = models.PostTag.objects.get(slug=self.kwargs['tag']).title
        context['title'] = f'Posts with {selected_tag_title} Tag'
        context['navbar'] = 'blog'
        return context


class BlogCategoryView(ListView):
    model = models.Post
    template_name = 'blog/home.html'
    paginate_by = 5

    def get_queryset(self):
        return models.PostCategory.objects.get(slug=self.kwargs['category']).post_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.PostCategory.objects.all()
        context['tags'] = models.PostTag.get_all_with_size()
        context['archives'] = models.Post.get_archives()
        context['popular_posts'] = models.Post.get_popular_posts()
        selected_category_title = models.PostCategory.objects.get(slug=self.kwargs['category']).title
        context['title'] = f'Posts with {selected_category_title} Category'
        context['navbar'] = 'blog'
        return context


def LikePostView(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    if request.user.is_authenticated:
        user = request.user
        post.liked_by.add(user)
        messages.success(request, 'Thanks for your feedback!')
        return HttpResponseRedirect(reverse('blog:post', kwargs={'slug': post.slug}))
    else:
        return HttpResponseRedirect(f'{reverse("users:signin")}?next={reverse("like_post", kwargs={"post_id": post_id})}')
