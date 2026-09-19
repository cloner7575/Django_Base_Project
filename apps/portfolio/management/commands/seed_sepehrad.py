"""Seed demo content for تابلوسازی سپهراد (inspired by public neonsepehrad listings)."""

from __future__ import annotations

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.blog.models import Post
from apps.contact.models import ConsultationRequest
from apps.portfolio.models import Category, Project

CATEGORIES: list[tuple[str, str]] = [
    ("تابلو نئون", "neon"),
    ("کافه و رستوران", "cafe-restaurant"),
    ("فروشگاه و بوتیک", "shop-boutique"),
    ("حروف برجسته", "channel-letters"),
]

PROJECTS: list[dict[str, object]] = [
    {
        "title": "تابلو نئون کافه رباط‌کریم",
        "slug": "neon-cafe-robat-karim",
        "summary": "نئون LED سفارشی با طرح نام کافه برای ویترین و فضای داخلی.",
        "description": (
            "طراحی و ساخت تابلو نئون LED برای یک کافه در رباط‌کریم. "
            "پس از تأیید طرح، نوار نئون روی پایه برش‌خورده نصب و منبع تغذیه "
            "ایمن‌سازی شد. رنگ‌بندی گرم برای فضای شبانه انتخاب شد."
        ),
        "category": "cafe-restaurant",
        "client_name": "کافه محلی رباط‌کریم",
        "is_featured": True,
    },
    {
        "title": "نئون Open برای بوتیک",
        "slug": "neon-open-boutique",
        "summary": "تابلو Open کلاسیک با نور فیروزه‌ای برای ویترین پوشاک.",
        "description": (
            "ساخت تابلو نئون Open با فونت خوانا و نور فیروزه‌ای؛ "
            "مناسب مغازه‌ها و بوتیک‌هایی که می‌خواهند در شب هم دیده شوند."
        ),
        "category": "shop-boutique",
        "client_name": "بوتیک پوشاک",
        "is_featured": True,
    },
    {
        "title": "تابلو نئون فست‌فود",
        "slug": "neon-fastfood",
        "summary": "لوگوی نورانی منوی فست‌فود با رنگ‌های پرانرژی.",
        "description": (
            "اجرای تابلو نئون با الهام از منوی فست‌فود؛ ترکیب رنگ‌های گرم "
            "برای جذب نگاه از فاصله و نصب روی نمای مغازه."
        ),
        "category": "neon",
        "client_name": "فست‌فود محلی",
        "is_featured": True,
    },
    {
        "title": "نئون سالن زیبایی",
        "slug": "neon-beauty-salon",
        "summary": "تابلو صورتی ملایم برای سالن زیبایی و آرایشگاه.",
        "description": (
            "طراحی اختصاصی نام سالن با نئون LED نرم؛ مناسب فضای داخلی و عکاسی مشتریان."
        ),
        "category": "neon",
        "client_name": "سالن زیبایی",
        "is_featured": True,
    },
    {
        "title": "حروف برجسته پلکسی مغازه",
        "slug": "plexiglass-channel-letters",
        "summary": "حروف برجسته پلکسی با نور پس‌زمینه برای تابلو سردر.",
        "description": (
            "ساخت و نصب حروف برجسته پلکسی روی زیرسازی آلومینیومی؛ "
            "نور پس‌زمینه برای خوانایی در شب و دوام در فضای باز رباط‌کریم."
        ),
        "category": "channel-letters",
        "client_name": "فروشگاه زنجیره‌ای محلی",
        "is_featured": False,
    },
    {
        "title": "تابلو نئون باشگاه ورزشی",
        "slug": "neon-gym",
        "summary": "شعار انگیزشی نورانی برای فضای باشگاه.",
        "description": (
            "اجرای تابلو نئون متنی برای دیوار باشگاه؛ فونت ضخیم و نور قوی "
            "برای حس انرژی در فضای تمرین."
        ),
        "category": "neon",
        "client_name": "باشگاه ورزشی",
        "is_featured": False,
    },
]

POSTS: list[dict[str, object]] = [
    {
        "title": "آموزش ساخت تابلو نئون در خانه",
        "slug": "learning-how-to-make-a-neon-sign-at-home",
        "excerpt": (
            "از طراحی تا برش نوار LED و سیم‌کشی — مسیر ساخت یک تابلو نئون ساده در خانه."
        ),
        "body": (
            "تابلوهای نئون رنگارنگ که در فروشگاه‌ها و کافه‌ها می‌بینید، "
            "با نوار نئون LED و کمی ابزار خانگی هم قابل ساخت‌اند.\n\n"
            "در این آموزش با اصول طراحی نئون، انتخاب الگو و رنگ، "
            "آشنایی با ابزار (نوار نئون LED، منبع تغذیه، چسب حرارتی) "
            "و مراحل برش، اتصال و نصب آشنا می‌شوید.\n\n"
            "اگر می‌خواهید طرح حرفه‌ای‌تر داشته باشید، می‌توانید از "
            "مشاوره حضوری تابلوسازی سپهراد در رباط‌کریم استفاده کنید "
            "یا برای سفارش آماده با ما تماس بگیرید."
        ),
        "days_ago": 30,
    },
    {
        "title": "چگونه طرح نئون کافه و رستوران را انتخاب کنیم؟",
        "slug": "neon-design-for-cafe-restaurant",
        "excerpt": (
            "نکات انتخاب فونت، رنگ و اندازه تابلو نئون برای فضای کافه و رستوران."
        ),
        "body": (
            "برای کافه و رستوران، تابلو باید هم در روز خوانا باشد و هم شب "
            "فضا را گرم کند. فونت ساده، کنتراست با دیوار، و رنگ نزدیک به "
            "هویت برند معمولاً نتیجه بهتری می‌دهد.\n\n"
            "اندازه را با فاصله دید مشتری تنظیم کنید؛ ویترین کوچک به تابلو "
            "جمع‌وجور نیاز دارد تا شلوغ نشود.\n\n"
            "در مجموعه سپهراد فایل‌های لایه باز و نمونه‌های آماده برای "
            "کافه، رستوران و آبمیوه‌فروشی هم در دسترس است تا سریع‌تر "
            "به طرح نهایی برسید."
        ),
        "days_ago": 14,
    },
    {
        "title": "تفاوت نئون شیشه‌ای و نئون LED انعطاف‌پذیر",
        "slug": "glass-neon-vs-flex-led",
        "excerpt": "مقایسه دوام، مصرف برق، هزینه و نگهداری دو نوع رایج تابلو نئون.",
        "body": (
            "نئون شیشه‌ای کلاسیک ظاهر خاص دارد اما شکننده و پرهزینه‌تر است. "
            "نئون LED انعطاف‌پذیر مصرف کمتر، نصب آسان‌تر و ایمنی بالاتر دارد "
            "و برای اکثر مغازه‌ها و سفارش‌های خانگی گزینه عملی‌تری است.\n\n"
            "اگر بین این دو مردد هستید، با شماره ۰۹۱۲۶۶۵۵۳۷۹ تماس بگیرید "
            "تا با توجه به بودجه و محل نصب راهنمایی‌تان کنیم."
        ),
        "days_ago": 7,
    },
]

SAMPLE_LEADS: list[dict[str, str]] = [
    {
        "name": "رضا محمدی",
        "phone": "09121112233",
        "email": "reza@example.com",
        "service_interest": "تابلو نئون کافه",
        "message": "برای کافه جدیدم تابلو نئون می‌خواهم. لطفاً قیمت حدودی بگویید.",
    },
]


class Command(BaseCommand):
    help = "Seed mock portfolio, blog, and sample leads for تابلوسازی سپهراد"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing portfolio/blog/contact demo rows before seeding",
        )

    @transaction.atomic
    def handle(self, *args: object, **options: object) -> None:
        if options["flush"]:
            ConsultationRequest.objects.all().delete()
            Post.objects.all().delete()
            Project.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write("Cleared existing portfolio, blog, and contact rows.")

        categories = {
            slug: Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name},
            )[0]
            for name, slug in CATEGORIES
        }
        self.stdout.write(f"Categories: {len(categories)}")

        for item in PROJECTS:
            category_slug = str(item["category"])
            project, created = Project.objects.update_or_create(
                slug=str(item["slug"]),
                defaults={
                    "title": str(item["title"]),
                    "summary": str(item["summary"]),
                    "description": str(item["description"]),
                    "category": categories[category_slug],
                    "client_name": str(item["client_name"]),
                    "is_published": True,
                    "is_featured": bool(item["is_featured"]),
                },
            )
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  {verb} project: {project.title}")

        now = timezone.now()
        for item in POSTS:
            published_at = now - timedelta(days=int(item["days_ago"]))
            post, created = Post.objects.update_or_create(
                slug=str(item["slug"]),
                defaults={
                    "title": str(item["title"]),
                    "excerpt": str(item["excerpt"]),
                    "body": str(item["body"]),
                    "is_published": True,
                    "published_at": published_at,
                },
            )
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  {verb} post: {post.title}")

        for item in SAMPLE_LEADS:
            lead, created = ConsultationRequest.objects.get_or_create(
                phone=item["phone"],
                name=item["name"],
                defaults={
                    "email": item["email"],
                    "service_interest": item["service_interest"],
                    "message": item["message"],
                    "is_read": False,
                },
            )
            verb = "Created" if created else "Kept"
            self.stdout.write(f"  {verb} lead: {lead.name}")

        self.stdout.write(self.style.SUCCESS("Sepahrad mock data ready."))
