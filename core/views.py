from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpRequest
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import Post


def list_post(request: HttpRequest):
    posts = Post.published.all()
    return render(request, "core/post/list.html", {"posts": posts})


def post_detail(request: HttpRequest, year: int, month: int, day: int, post):
    post = get_object_or_404(
        Post,
        slug=post, 
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED)
    return render(request, "core/post/detail.html", {"post": post})
