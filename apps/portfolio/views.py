from __future__ import annotations

from django.db.models import Prefetch, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.portfolio.models import Category, Project, ProjectImage


def project_list(request: HttpRequest) -> HttpResponse:
    category_slug = request.GET.get("category", "").strip()
    projects: QuerySet[Project] = (
        Project.objects.published().select_related("category").order_by("-created_at")
    )
    categories = Category.objects.filter(projects__is_published=True).distinct()
    active_category: Category | None = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        projects = projects.filter(category=active_category)

    return render(
        request,
        "portfolio/list.html",
        {
            "projects": projects,
            "categories": categories,
            "active_category": active_category,
        },
    )


def project_detail(request: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(
        Project.objects.published()
        .select_related("category")
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ProjectImage.objects.order_by("sort_order", "id"),
            )
        ),
        slug=slug,
    )
    return render(request, "portfolio/detail.html", {"project": project})
