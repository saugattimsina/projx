from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/list.html"
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/detail.html"


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/update.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    context_object_name = "post"
    template_name = "posts/delete.html"
    success_url = reverse_lazy("post_list")
