from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from apps.portfolio.content import (
    ARCHITECTURE_CONCEPTS,
    ARCHITECTURE_FLOW,
    BUILD_STEPS,
    EMAIL,
    EXPERIENCE,
    GITHUB_HANDLE,
    GITHUB_URL,
    LINKEDIN_URL,
    PROJECTS,
    STACK_GROUPS,
    STATS,
    get_project,
    resume_url,
)
from apps.portfolio.forms import ContactForm
from apps.portfolio.services import create_contact_message


def _home_context(form: ContactForm) -> dict[str, object]:
    return {
        "projects": PROJECTS,
        "experience": EXPERIENCE,
        "stack_groups": STACK_GROUPS,
        "build_steps": BUILD_STEPS,
        "stats": STATS,
        "architecture_flow": ARCHITECTURE_FLOW,
        "architecture_concepts": ARCHITECTURE_CONCEPTS,
        "github_url": GITHUB_URL,
        "github_handle": GITHUB_HANDLE,
        "linkedin_url": LINKEDIN_URL,
        "contact_email": EMAIL,
        "resume_url": resume_url(),
        "contact_form": form,
    }


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "portfolio/home.html", _home_context(ContactForm()))


def case_study(request: HttpRequest, slug: str) -> HttpResponse:
    project = get_project(slug)
    if project is None:
        raise Http404(_("Project not found."))

    return render(
        request,
        "portfolio/case_study.html",
        {
            "project": project,
            "projects": PROJECTS,
            "github_url": GITHUB_URL,
            "linkedin_url": LINKEDIN_URL,
            "resume_url": resume_url(),
        },
    )


@require_http_methods(["POST"])
def contact(request: HttpRequest) -> HttpResponse:
    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            "portfolio/home.html",
            _home_context(form),
            status=400,
        )

    create_contact_message(
        name=form.cleaned_data["name"],
        email=form.cleaned_data["email"],
        message=form.cleaned_data["message"],
    )
    messages.success(
        request,
        _("Thanks — your message was sent. I'll get back to you soon."),
    )
    return redirect(f"{reverse('portfolio:home')}#contact")
