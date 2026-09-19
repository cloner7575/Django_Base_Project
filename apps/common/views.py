from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from apps.blog.models import Post
from apps.portfolio.models import Project


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


def home(request: HttpRequest) -> HttpResponse:
    featured_projects = list(Project.objects.featured().select_related("category")[:6])
    recent_posts = list(Post.objects.published().order_by("-published_at")[:3])
    return render(
        request,
        "pages/home.html",
        {
            "featured_projects": featured_projects,
            "recent_posts": recent_posts,
        },
    )
