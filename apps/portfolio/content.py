"""Static portfolio content — projects, experience, stack.

Translatable strings use gettext_lazy so templates and Python share one catalog.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _

GITHUB_URL = "https://github.com/cloner7575"
GITHUB_HANDLE = "@cloner7575"
LINKEDIN_URL = "https://www.linkedin.com/in/mohammad-zare-5b3630154"
EMAIL = "mrzjkb1375@gmail.com"
RESUME_STATIC_PATH = "files/mrz-resume.pdf"
BRAND_MARK = "MRZ"
PERSON_NAME = _("Mohammadreza Zare")
PERSON_NAME_FA = "محمدرضا زارع"


@dataclass(frozen=True, slots=True)
class Project:
    slug: str
    title: str
    subtitle: str
    summary: str
    stack: tuple[str, ...]
    cta_label: str
    problem: str
    role: str
    architecture: tuple[str, ...]
    outcomes: tuple[str, ...]
    mockup: str  # CSS mockup variant key


PROJECTS: tuple[Project, ...] = (
    Project(
        slug="rahatsell",
        title="RahatSell",
        subtitle=_("Messaging-first commerce platform for sellers."),
        summary=_(
            "A commerce platform designed to help sellers manage products, "
            "orders and customer conversations through messaging platforms."
        ),
        stack=("Django", "DRF", "PostgreSQL", "Telegram/Bale"),
        cta_label=_("View Case Study"),
        problem=_(
            "Sellers needed to run product catalogs and order flows inside "
            "messaging apps without a fragile, ad-hoc bot script."
        ),
        role=_(
            "Designed and built the Django backend, REST surfaces, and "
            "messaging integrations that connect conversations to orders."
        ),
        architecture=(
            _("Modular catalog and order domains behind DRF endpoints."),
            _("Telegram/Bale adapters isolated from core business logic."),
            _("PostgreSQL models for products, conversations, and orders."),
            _("Authentication and seller-scoped permissions for API access."),
        ),
        outcomes=(
            _("Sellers manage inventory and orders from messaging threads."),
            _("Backend stays testable with clear service boundaries."),
        ),
        mockup="rahatsell",
    ),
    Project(
        slug="bimtec",
        title="Bimtec",
        subtitle=_("AI-powered insurance platform."),
        summary=_(
            "A digital insurance platform focused on simplifying "
            "insurance-related workflows and integrating AI-assisted services."
        ),
        stack=("Django", "REST API", "AI Integration", "PostgreSQL"),
        cta_label=_("View Case Study"),
        problem=_(
            "Insurance workflows were scattered across manual steps; the "
            "product needed a reliable API layer plus AI-assisted services."
        ),
        role=_(
            "Built backend APIs, data models, and integration points for "
            "AI-assisted insurance features on Django and PostgreSQL."
        ),
        architecture=(
            _("REST API for policies, quotes, and workflow states."),
            _("Service layer for AI provider calls with clear failure modes."),
            _("PostgreSQL as the source of truth for insurance records."),
            _("Auth-gated endpoints for staff and partner clients."),
        ),
        outcomes=(
            _("Insurance flows expose a consistent API surface."),
            _("AI features plug in without coupling to request handlers."),
        ),
        mockup="bimtec",
    ),
    Project(
        slug="insurance-api",
        title=_("Insurance API Architecture"),
        subtitle=_("Modular backend for insurance services."),
        summary=_(
            "Backend architecture for insurance services with modular APIs, "
            "authentication, business logic and scalable service structure."
        ),
        stack=("Django", "DRF", "PostgreSQL", "Auth"),
        cta_label=_("View Architecture"),
        problem=_(
            "Insurance capabilities needed a modular API layout that could "
            "grow without collapsing into a single fat application."
        ),
        role=_(
            "Designed the service boundaries, authentication model, and "
            "business-logic layer for a scalable insurance API platform."
        ),
        architecture=(
            _("API gateway-style entry into versioned Django/DRF services."),
            _("Domain modules for auth, policies, and external providers."),
            _("RBAC and token-based authentication for clients."),
            _("Clear separation between transport, domain, and persistence."),
        ),
        outcomes=(
            _("New insurance capabilities ship as modules, not rewrites."),
            _("Auth and business rules stay auditable in one place."),
        ),
        mockup="insurance",
    ),
    Project(
        slug="dev2dev",
        title=_("Web Development Platform"),
        subtitle="Dev2Dev",
        summary=_(
            "A software development platform focused on delivering modern "
            "web products and backend solutions."
        ),
        stack=("Django", "Backend Architecture", "API"),
        cta_label=_("View Case Study"),
        problem=_(
            "Delivery work needed a shared backend foundation for modern "
            "web products instead of one-off project scaffolds."
        ),
        role=_(
            "Owned backend architecture and API design for product delivery "
            "across client web projects."
        ),
        architecture=(
            _("Reusable Django project patterns for multi-client delivery."),
            _("REST APIs tailored to each product's domain model."),
            _("Maintainable service and selector boundaries."),
        ),
        outcomes=(
            _("Faster delivery with consistent backend structure."),
            _("Clients get production-ready APIs, not prototypes."),
        ),
        mockup="dev2dev",
    ),
)


@dataclass(frozen=True, slots=True)
class Experience:
    company: str
    role: str
    period: str
    bullets: tuple[str, ...]


EXPERIENCE: tuple[Experience, ...] = (
    Experience(
        company="RahatSell",
        role=_("Backend Engineer"),
        period="2024 — Present",
        bullets=(
            _("Designed and developed RESTful APIs using Django REST Framework."),
            _(
                "Implemented business logic and database architecture for "
                "messaging-first commerce."
            ),
            _("Integrated Telegram and Bale so sellers manage orders in-chat."),
            _("Improved maintainability through modular backend architecture."),
        ),
    ),
    Experience(
        company="Bimtec / Insurance platforms",
        role=_("Backend Engineer"),
        period="2023 — 2024",
        bullets=(
            _(
                "Built insurance REST APIs with authentication and clear "
                "domain boundaries."
            ),
            _("Integrated AI-assisted services behind stable service interfaces."),
            _("Modeled PostgreSQL schemas for policies, workflows, and audits."),
        ),
    ),
    Experience(
        company="Dev2Dev & freelance delivery",
        role=_("Software Engineer"),
        period="2022 — 2023",
        bullets=(
            _("Delivered Django backends and APIs for client web products."),
            _("Owned data modeling, auth, and production-ready error handling."),
            _("Collaborated with product stakeholders on real business logic."),
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class StackGroup:
    title: str
    items: tuple[str, ...]


STACK_GROUPS: tuple[StackGroup, ...] = (
    StackGroup(_("Backend"), ("Python", "Django", "Django REST Framework", "FastAPI")),
    StackGroup(_("Database"), ("PostgreSQL", "Redis")),
    StackGroup(_("Infrastructure"), ("Linux", "Docker", "Nginx", "Git")),
    StackGroup(
        _("Architecture"),
        (
            "REST API",
            "Authentication",
            "RBAC",
            "Background Tasks",
            "Caching",
            "Database Design",
        ),
    ),
    StackGroup(
        _("Integrations"),
        ("Telegram", "Bale", "Payment APIs", "Third-party APIs", "AI APIs"),
    ),
)


BUILD_STEPS: tuple[tuple[str, str, str], ...] = (
    ("01", _("Understand"), _("Understand the business problem before writing code.")),
    ("02", _("Design"), _("Design clean architecture, APIs and data models.")),
    ("03", _("Build"), _("Write maintainable, testable and production-ready code.")),
    ("04", _("Improve"), _("Monitor, refactor and continuously improve the system.")),
)


STATS: tuple[tuple[str, str], ...] = (
    ("3.5+", _("Years Experience")),
    ("Django", _("Primary Framework")),
    ("REST API", _("Backend Focus")),
    ("Production", _("Real-world Projects")),
)


ARCHITECTURE_FLOW: tuple[str, ...] = (
    "Client",
    "API Gateway",
    "Django / DRF",
    "Business Logic",
    "PostgreSQL",
    "External Services",
)

ARCHITECTURE_CONCEPTS: tuple[str, ...] = (
    _("Clean Architecture"),
    _("API Design"),
    _("Database Modeling"),
    _("Authentication"),
    _("Scalable Services"),
)


def get_project(slug: str) -> Project | None:
    for project in PROJECTS:
        if project.slug == slug:
            return project
    return None


def resume_url() -> str:
    """Public URL for the hosted resume PDF (hashed in production)."""
    from django.templatetags.static import static

    return static(RESUME_STATIC_PATH)
