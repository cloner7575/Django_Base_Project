from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.blog.models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.published().order_by("-published_at")
    return render(request, "blog/list.html", {"posts": posts})


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post.objects.published(), slug=slug)
    return render(request, "blog/detail.html", {"post": post})
