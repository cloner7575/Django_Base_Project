from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.shop.adapters import ensure_default_variant
from apps.shop.models import (
    Category,
    HeroSlide,
    Product,
    ProductVariant,
    SiteFeature,
    Testimonial,
)

CATEGORIES = [
    {"name": "ترشیجات", "slug": "torshiijat", "subtitle": "ترشی‌های سنتی"},
    {"name": "مربا و مرباجات", "slug": "morabba", "subtitle": "صبحانه خانگی"},
    {"name": "لبنیات خانگی", "slug": "labaniat", "subtitle": "از شیر محلی"},
    {"name": "خشکبار و ادویه", "slug": "khoshkbar", "subtitle": "طعم‌دهنده محفل"},
]

PRODUCTS = [
    {
        "category_slug": "torshiijat",
        "name": "ترشی مخلوط خانگی",
        "slug": "torshi-makhlut",
        "description": "ترشی مخلوط سنتی با خیار، هویج و گل‌کلم.",
        "price": 185000,
        "sale_price": 165000,
        "is_new": True,
        "is_sale": True,
        "best_seller": True,
        "variants": [
            {"size": "شیشه ۵۰۰ گرم", "stock": 30, "price": 165000},
            {
                "size": "شیشه ۷۰۰ گرم",
                "stock": 20,
                "price": 185000,
                "sale_price": 165000,
            },
        ],
    },
    {
        "category_slug": "torshiijat",
        "name": "ترشی لیته بادمجان",
        "slug": "torshi-liteh",
        "description": "لیته بادمجان کبابی با طعم تند ملایم.",
        "price": 165000,
        "best_seller": True,
        "variants": [{"size": "استاندارد", "stock": 35}],
    },
    {
        "category_slug": "torshiijat",
        "name": "شور خیار درجه یک",
        "slug": "shoor-khiar",
        "description": "خیارشور ترد و کم‌نمک.",
        "price": 120000,
        "is_new": True,
        "variants": [
            {"size": "شیشه کوچک", "stock": 40, "price": 98000},
            {"size": "شیشه بزرگ", "stock": 25, "price": 120000},
        ],
    },
    {
        "category_slug": "torshiijat",
        "name": "سیر ترشی کهنه",
        "slug": "sir-torshi",
        "description": "سیر ترشی کهنه با رنگ عنابی.",
        "price": 220000,
        "variants": [{"size": "استاندارد", "stock": 18}],
    },
    {
        "category_slug": "morabba",
        "name": "مربای به خانگی",
        "slug": "morabba-beh",
        "description": "مربای به طبیعی بدون رنگ مصنوعی.",
        "price": 195000,
        "variants": [{"size": "شیشه ۴۵۰ گرم", "stock": 28}],
    },
    {
        "category_slug": "morabba",
        "name": "مربای آلبالو",
        "slug": "morabba-albaloo",
        "description": "آلبالوی تازه فصل.",
        "price": 175000,
        "is_sale": True,
        "sale_price": 155000,
        "variants": [{"size": "استاندارد", "stock": 22, "sale_price": 155000}],
    },
    {
        "category_slug": "labaniat",
        "name": "ماست چکیده خانگی",
        "slug": "mast-chekideh",
        "description": "ماست چکیده غلیظ از شیر محلی.",
        "price": 98000,
        "best_seller": True,
        "variants": [{"size": "۵۰۰ گرم", "stock": 45}],
    },
    {
        "category_slug": "labaniat",
        "name": "دوغ سنتی نعنایی",
        "slug": "dough-sonati",
        "description": "دوغ خانگی با نعنا و گلپر.",
        "price": 75000,
        "variants": [
            {"size": "۱ لیتر", "stock": 50},
            {"size": "۲ لیتر", "stock": 20, "price": 130000},
        ],
    },
    {
        "category_slug": "khoshkbar",
        "name": "ادویه ترشی محفل",
        "slug": "advieh-torshi",
        "description": "مخلوط ادویه مخصوص ترشی خانگی.",
        "price": 89000,
        "variants": [{"size": "۱۰۰ گرم", "stock": 55}],
    },
    {
        "category_slug": "khoshkbar",
        "name": "رب انار محلی",
        "slug": "rob-anar",
        "description": "رب انار ترش و غلیظ.",
        "price": 210000,
        "variants": [{"size": "استاندارد", "stock": 16}],
    },
]


class Command(BaseCommand):
    help = "Seed Mahfel shop demo data (NightRuby-class catalog)"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--with-demo-user",
            action="store_true",
            help="Create demo / demo-pass-123 customer",
        )
        parser.add_argument(
            "--with-staff",
            action="store_true",
            help="Create staff / staff-pass-123 for /panel/",
        )

    @transaction.atomic
    def handle(self, *args: object, **options: object) -> None:
        categories: dict[str, Category] = {}
        for item in CATEGORIES:
            category, _ = Category.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["name"],
                    "subtitle": item["subtitle"],
                    "is_active": True,
                },
            )
            categories[category.slug] = category

        for item in PRODUCTS:
            category = categories[str(item["category_slug"])]
            product, _ = Product.objects.update_or_create(
                slug=str(item["slug"]),
                defaults={
                    "category": category,
                    "name": str(item["name"]),
                    "description": str(item["description"]),
                    "price": int(item["price"]),
                    "sale_price": item.get("sale_price"),
                    "stock": 0,
                    "is_active": True,
                    "is_new": bool(item.get("is_new")),
                    "is_sale": bool(item.get("is_sale")),
                    "best_seller": bool(item.get("best_seller")),
                },
            )
            product.variants.all().delete()
            variants = item.get("variants") or []
            if not variants:
                ensure_default_variant(product)
            else:
                for variant in variants:
                    ProductVariant.objects.create(
                        product=product,
                        size=str(variant["size"]),
                        stock=int(variant.get("stock", 10)),
                        price=variant.get("price"),
                        sale_price=variant.get("sale_price"),
                    )
            self.stdout.write(f"Product: {product.name}")

        HeroSlide.objects.update_or_create(
            headline="محصولات خانگی محفل",
            defaults={
                "badge": "طعم خانه",
                "headline_accent": "تازه و سنتی",
                "subtitle": "ترشی، مربا و لبنیات خانگی با ارسال مطمئن",
                "cta_label": "مشاهده فروشگاه",
                "cta_url": "/shop/products/",
                "theme": "light",
                "is_active": True,
                "sort_order": 0,
            },
        )
        features = [
            ("مواد اولیه خانگی", "بدون افزودنی مصنوعی"),
            ("طعم تازه", "دستورهای سنتی فصلی"),
            ("سفارش آسان", "پرداخت امن زرین‌پال"),
        ]
        for i, (title, subtitle) in enumerate(features):
            SiteFeature.objects.update_or_create(
                title=title,
                defaults={"subtitle": subtitle, "sort_order": i, "is_active": True},
            )
        Testimonial.objects.update_or_create(
            name="سارا م.",
            defaults={
                "text": "ترشی مخلوط‌شون عطر خونه مادربزرگ رو داره.",
                "rating": 5,
                "initials": "سم",
                "is_active": True,
            },
        )

        user_model = get_user_model()
        if options.get("with_demo_user"):
            user, created = user_model.objects.get_or_create(
                username="demo",
                defaults={"email": "demo@mahfel.local"},
            )
            if created:
                user.set_password("demo-pass-123")
                user.save()
                self.stdout.write("demo / demo-pass-123")

        if options.get("with_staff"):
            staff, created = user_model.objects.get_or_create(
                username="staff",
                defaults={"email": "staff@mahfel.local", "is_staff": True},
            )
            staff.is_staff = True
            if created:
                staff.set_password("staff-pass-123")
            staff.save()
            self.stdout.write("staff / staff-pass-123")

        self.stdout.write(self.style.SUCCESS("Seed complete."))
