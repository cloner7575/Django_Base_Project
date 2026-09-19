from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog.adapters import ensure_default_variant
from apps.catalog.models import (
    Category,
    Collection,
    HeroSlide,
    Product,
    ProductColor,
    ProductVariant,
    SiteFeature,
    Testimonial,
)

CATEGORIES = [
    {"name": "شمع", "slug": "shama", "subtitle": "عطر و نور ملایم"},
    {"name": "سنگ مصنوعی", "slug": "sang", "subtitle": "بافت و دکور"},
    {"name": "ست هدیه", "slug": "set", "subtitle": "بسته‌های آماده"},
]

PRODUCTS = [
    {
        "category_slug": "shama",
        "name": "شمع معطر وانیل",
        "slug": "sham-vanilla",
        "description": "شمع سویا با رایحه وانیل گرم؛ مناسب فضای نشیمن.",
        "price": 185000,
        "sale_price": 165000,
        "is_new": True,
        "is_sale": True,
        "best_seller": True,
        "variants": [
            {"size": "کوچک", "stock": 30, "price": 145000},
            {"size": "متوسط", "stock": 25, "price": 165000},
            {"size": "بزرگ", "stock": 18, "price": 185000, "sale_price": 165000},
        ],
    },
    {
        "category_slug": "shama",
        "name": "شمع گل سرخ",
        "slug": "sham-rose",
        "description": "شمع دست‌ساز با رایحه گل سرخ و رنگ صورتی ملایم.",
        "price": 195000,
        "best_seller": True,
        "variants": [
            {"size": "استاندارد", "stock": 35},
            {"size": "دوقلو", "stock": 20, "price": 320000},
        ],
    },
    {
        "category_slug": "shama",
        "name": "شمع ستونی کرم",
        "slug": "sham-column",
        "description": "شمع ستونی بدون عطر برای میز شام و دکوراسیون.",
        "price": 120000,
        "is_new": True,
        "variants": [
            {"size": "۲۰ سانتی", "stock": 40, "price": 98000},
            {"size": "۳۰ سانتی", "stock": 25, "price": 120000},
        ],
    },
    {
        "category_slug": "shama",
        "name": "شمع جار کهربایی",
        "slug": "sham-jar",
        "description": "شمع داخل شیشه کهربایی با فتیله چوبی.",
        "price": 220000,
        "variants": [{"size": "استاندارد", "stock": 22}],
    },
    {
        "category_slug": "sang",
        "name": "سنگ رز کوارتز مصنوعی",
        "slug": "sang-rose-quartz",
        "description": "سنگ دکوراتیو با بافت رز کوارتز برای قفسه و میز.",
        "price": 245000,
        "best_seller": True,
        "variants": [
            {"size": "تک‌عددی", "stock": 28},
            {"size": "ست ۳ تایی", "stock": 15, "price": 620000},
        ],
    },
    {
        "category_slug": "sang",
        "name": "سنگ اونیکس مشکی",
        "slug": "sang-onyx",
        "description": "سنگ مصنوعی براق با جلوه اونیکس برای کنتراست دکور.",
        "price": 275000,
        "is_sale": True,
        "sale_price": 245000,
        "variants": [{"size": "متوسط", "stock": 20, "sale_price": 245000}],
    },
    {
        "category_slug": "sang",
        "name": "سنگ آمیتیست روشن",
        "slug": "sang-amethyst",
        "description": "سنگ مصنوعی بنفش روشن؛ مناسب کنار شمع صورتی.",
        "price": 210000,
        "is_new": True,
        "variants": [{"size": "کوچک", "stock": 32}, {"size": "متوسط", "stock": 18}],
    },
    {
        "category_slug": "sang",
        "name": "سنگ مرمر سفید",
        "slug": "sang-marble",
        "description": "سنگ مصنوعی با رگه‌های مرمر سفید و کرم.",
        "price": 198000,
        "variants": [{"size": "استاندارد", "stock": 26}],
    },
    {
        "category_slug": "set",
        "name": "ست شمع و سنگ صورتی",
        "slug": "set-pink",
        "description": "بسته‌بندی هدیه: دو شمع معطر + یک سنگ رز کوارتز.",
        "price": 520000,
        "sale_price": 480000,
        "is_sale": True,
        "best_seller": True,
        "variants": [{"size": "جعبه هدیه", "stock": 14, "sale_price": 480000}],
    },
    {
        "category_slug": "set",
        "name": "ست میز شام",
        "slug": "set-dinner",
        "description": "چهار شمع ستونی کرم + دو سنگ مرمر کوچک.",
        "price": 450000,
        "variants": [{"size": "جعبه هدیه", "stock": 12}],
    },
]


class Command(BaseCommand):
    help = "Seed Fitile Shop demo data (candles & artificial stones)"

    def add_arguments(self, parser) -> None:  # type: ignore[no-untyped-def]
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
            categories[item["slug"]] = category

        for index, item in enumerate(PRODUCTS, start=1):
            category = categories[item["category_slug"]]
            product, _ = Product.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "category": category,
                    "name": item["name"],
                    "description": item["description"],
                    "price": item["price"],
                    "sale_price": item.get("sale_price"),
                    "stock": 10,
                    "is_active": True,
                    "is_new": item.get("is_new", False),
                    "is_sale": item.get("is_sale", False),
                    "best_seller": item.get("best_seller", False),
                },
            )
            image_path = Path(settings.MEDIA_ROOT) / "products" / f"p{index}.jpg"
            if image_path.exists() and not product.image:
                with image_path.open("rb") as handle:
                    product.image.save(f"{product.slug}.jpg", File(handle), save=True)
            elif image_path.exists():
                with image_path.open("rb") as handle:
                    product.image.save(f"{product.slug}.jpg", File(handle), save=True)
            product.variants.all().delete()
            for variant in item.get("variants", []):
                ProductVariant.objects.create(
                    product=product,
                    size=variant["size"],
                    stock=variant.get("stock", 10),
                    price=variant.get("price"),
                    sale_price=variant.get("sale_price"),
                )
            ensure_default_variant(product)

        HeroSlide.objects.update_or_create(
            sort_order=0,
            defaults={
                "badge": "نور و بافت خانه",
                "headline": "فیتیله شاپ",
                "headline_accent": "شمع و سنگ مصنوعی",
                "subtitle": "دکور گرم برای خانه و هدیه — ارسال مطمئن",
                "cta_label": "مشاهده فروشگاه",
                "cta_url": "/shop/products/",
                "theme": "photo",
                "is_active": True,
            },
        )
        HeroSlide.objects.update_or_create(
            sort_order=1,
            defaults={
                "badge": "هدیه خاص",
                "headline": "ست‌های آماده",
                "headline_accent": "شمع + سنگ",
                "subtitle": "بسته‌بندی زیبا برای هدیه تولد و خانه‌نو",
                "cta_label": "مشاهده ست‌ها",
                "cta_url": "/shop/products/?category=set",
                "theme": "light",
                "is_active": True,
            },
        )
        hero_path = Path(settings.MEDIA_ROOT) / "products" / "hero-fitile.jpg"
        if not hero_path.exists():
            hero_path = Path(settings.MEDIA_ROOT) / "hero-fitile.jpg"
        for slide in HeroSlide.objects.filter(is_active=True):
            if hero_path.exists():
                with hero_path.open("rb") as handle:
                    slide.image.save(
                        f"hero-{slide.sort_order}.jpg", File(handle), save=True
                    )

        warm = Collection.objects.update_or_create(
            slug="garm",
            defaults={
                "title": "مجموعه گرم",
                "subtitle": "شمع و بافت برای شب‌های آرام",
                "is_active": True,
            },
        )[0]
        soft = Collection.objects.update_or_create(
            slug="narm",
            defaults={
                "title": "مجموعه نرم",
                "subtitle": "صورتی و کرم برای دکور لطیف",
                "is_active": True,
            },
        )[0]
        for product in Product.objects.filter(category__slug="shama"):
            product.collections.add(warm)
        for product in Product.objects.filter(category__slug__in=["sang", "set"]):
            product.collections.add(soft)

        rose = Product.objects.filter(slug="sham-rose").first()
        if rose is not None:
            pink, _ = ProductColor.objects.update_or_create(
                product=rose,
                name="صورتی",
                defaults={"hex_code": "#C45A7A", "sort_order": 0},
            )
            cream, _ = ProductColor.objects.update_or_create(
                product=rose,
                name="کرم",
                defaults={"hex_code": "#E8DCC8", "sort_order": 1},
            )
            rose.variants.all().delete()
            ProductVariant.objects.create(
                product=rose, size="استاندارد", color=pink, stock=20
            )
            ProductVariant.objects.create(
                product=rose, size="استاندارد", color=cream, stock=15
            )
            ProductVariant.objects.create(
                product=rose, size="دوقلو", color=pink, stock=10, price=320000
            )

        features = [
            ("ارسال امن", "بسته‌بندی ضدضربه برای شمع و سنگ"),
            ("عطر طبیعی", "شمع‌های دست‌ساز با رایحه ملایم"),
            ("دکور ماندگار", "سنگ مصنوعی سبک و زیبا"),
        ]
        for index, (title, subtitle) in enumerate(features):
            SiteFeature.objects.update_or_create(
                title=title,
                defaults={"subtitle": subtitle, "sort_order": index, "is_active": True},
            )

        Testimonial.objects.update_or_create(
            name="سارا م.",
            defaults={
                "text": "ست شمع و سنگ صورتی‌شون برای هدیه عروسی عالی بود.",
                "rating": 5,
                "initials": "سم",
                "sort_order": 0,
                "is_active": True,
            },
        )

        user_model = get_user_model()
        if options.get("with_demo_user"):
            user, created = user_model.objects.get_or_create(
                username="demo",
                defaults={"email": "demo@fitile-shop.local"},
            )
            if created:
                user.set_password("demo-pass-123")
                user.save()
            self.stdout.write("demo / demo-pass-123")

        if options.get("with_staff"):
            staff, created = user_model.objects.get_or_create(
                username="staff",
                defaults={"email": "staff@fitile-shop.local", "is_staff": True},
            )
            if created or not staff.is_staff:
                staff.is_staff = True
                staff.set_password("staff-pass-123")
                staff.save()
            self.stdout.write("staff / staff-pass-123")

        self.stdout.write(self.style.SUCCESS("Seed complete."))
