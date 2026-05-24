"""
Seed the database with demo data for Orel Fashion.
Run: python manage.py seed
"""
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.accounts.models import User
from apps.catalog.models import Category, Color, Discount, Product, ProductImage, ProductVariant, Size
from apps.core.models import Branch, HeroContent

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with brand, products, branches, and demo users"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")
        self._seed_colors_sizes_categories()
        self._seed_hero()
        self._seed_branches()
        self._seed_products()
        self._seed_users()
        self.stdout.write(self.style.SUCCESS("Seed completed successfully."))

    def _seed_colors_sizes_categories(self):
        colors = [
            ("Black", "#1a1a1a"),
            ("White", "#f5f5f5"),
            ("Navy", "#1e3a5f"),
            ("Camel", "#c4a574"),
            ("Burgundy", "#722f37"),
            ("Stone", "#9a9a8e"),
        ]
        for name, hex_code in colors:
            Color.objects.get_or_create(name=name, defaults={"hex_code": hex_code})

        sizes = [("XS", 1), ("S", 2), ("M", 3), ("L", 4), ("XL", 5), ("XXL", 6)]
        for name, order in sizes:
            Size.objects.get_or_create(name=name, defaults={"sort_order": order})

        categories = [
            ("Coats", Category.Section.MEN),
            ("Trousers", Category.Section.MEN),
            ("Shirts", Category.Section.MEN),
            ("Dresses", Category.Section.WOMEN),
            ("Knitwear", Category.Section.WOMEN),
            ("Outerwear", Category.Section.WOMEN),
            ("Tops", Category.Section.KIDS),
            ("New Arrivals", Category.Section.NEW),
            ("Sale Items", Category.Section.SALE),
        ]
        for name, section in categories:
            Category.objects.get_or_create(name=name, section=section)

    def _seed_hero(self):
        HeroContent.objects.get_or_create(
            title="Autumn / Winter 2026",
            defaults={
                "subtitle": "Refined essentials for the modern wardrobe",
                "cta_text": "Explore Collection",
                "cta_link": "/shop/new/",
                "is_active": True,
                "sort_order": 0,
            },
        )

    def _seed_branches(self):
        branches = [
            {
                "name": "Orel Fashion — London Flagship",
                "address_line1": "42 Regent Street",
                "city": "London",
                "postcode": "W1B 5RA",
                "phone": "+44 20 7946 0123",
                "latitude": Decimal("51.510357"),
                "longitude": Decimal("-0.136439"),
                "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2483.0!2d-0.1364!3d51.5104!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1",
                "opening_hours": "Mon–Sat 10:00–20:00, Sun 12:00–18:00",
            },
            {
                "name": "Orel Fashion — Manchester",
                "address_line1": "18 King Street",
                "city": "Manchester",
                "postcode": "M2 6AZ",
                "phone": "+44 161 496 0456",
                "latitude": Decimal("53.480759"),
                "longitude": Decimal("-2.242631"),
                "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2374.0!2d-2.2426!3d53.4808!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1",
                "opening_hours": "Mon–Sat 10:00–19:00",
            },
            {
                "name": "Orel Fashion — Tehran",
                "address_line1": "Valiasr Street, No. 128",
                "city": "Tehran",
                "postcode": "19617",
                "country": "Iran",
                "phone": "+98 21 8876 2345",
                "latitude": Decimal("35.721858"),
                "longitude": Decimal("51.410341"),
                "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3239.0!2d51.4103!3d35.7219!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1",
                "opening_hours": "Sat–Thu 10:00–21:00",
            },
        ]
        for i, data in enumerate(branches):
            Branch.objects.get_or_create(name=data["name"], defaults={**data, "sort_order": i})

    def _seed_products(self):
        if Product.objects.exists():
            self.stdout.write("Products already exist, skipping product seed.")
            return

        men_cat = Category.objects.filter(section=Category.Section.MEN).first()
        women_cat = Category.objects.filter(section=Category.Section.WOMEN).first()
        colors = list(Color.objects.all()[:4])
        sizes = list(Size.objects.filter(name__in=["S", "M", "L", "XL"]))

        catalog = [
            ("Structured Wool Coat", "men", men_cat, True, Decimal("189.00")),
            ("Relaxed Linen Shirt", "men", men_cat, True, Decimal("59.00")),
            ("Tailored Pleat Trousers", "men", men_cat, False, Decimal("79.00")),
            ("Merino Crew Jumper", "men", men_cat, False, Decimal("89.00")),
            ("Slim Fit Denim", "men", men_cat, False, Decimal("69.00")),
            ("Silk Blend Evening Shirt", "men", men_cat, True, Decimal("99.00")),
            ("Oversized Trench", "women", women_cat, True, Decimal("219.00")),
            ("Midi Satin Dress", "women", women_cat, True, Decimal("129.00")),
            ("Cashmere Roll Neck", "women", women_cat, False, Decimal("149.00")),
            ("High Waist Wide Leg", "women", women_cat, False, Decimal("89.00")),
            ("Draped Blouse", "women", women_cat, True, Decimal("69.00")),
            ("Wool Blend Blazer", "women", women_cat, False, Decimal("159.00")),
        ]

        for i, (title, gender, category, is_new, base_price) in enumerate(catalog):
            product = Product.objects.create(
                title=title,
                description=f"Premium {title.lower()} crafted for Orel Fashion. "
                "Designed with refined silhouettes and exceptional fabrics.",
                category=category,
                gender=gender,
                is_new_arrival=is_new,
                is_active=True,
            )
            for idx, color in enumerate(colors[:3]):
                for j, size in enumerate(sizes):
                    price = base_price + Decimal(j * 5)
                    stock = 10 - (idx + j) % 12
                    ProductVariant.objects.create(
                        product=product,
                        color=color,
                        size=size,
                        price=price,
                        stock=max(0, stock),
                    )
            if i == 0:
                variant = product.variants.first()
                now = timezone.now()
                Discount.objects.create(
                    variant=variant,
                    percentage=20,
                    starts_at=now - timedelta(hours=1),
                    ends_at=now + timedelta(days=7),
                    label="Limited time deal",
                )

        # Extra products to fill grids
        for n in range(13, 45):
            cat = women_cat if n % 2 else men_cat
            Product.objects.create(
                title=f"Collection Piece {n:02d}",
                description="A timeless addition to your wardrobe.",
                category=cat,
                gender="women" if n % 2 else "men",
                is_active=True,
            )

    def _seed_users(self):
        if not User.objects.filter(email="admin@maisonatelier.com").exists():
            admin = User.objects.create_superuser(
                username="admin@maisonatelier.com",
                email="admin@maisonatelier.com",
                password="admin12345",
                first_name="Admin",
                last_name="User",
                phone_number="+440000000000",
            )
            admin.is_verified = True
            admin.save(update_fields=["is_verified"])
            self.stdout.write("Admin: admin@maisonatelier.com / admin12345")

        if not User.objects.filter(email="customer@example.com").exists():
            user = User.objects.create_user(
                username="customer@example.com",
                email="customer@example.com",
                password="customer123",
                first_name="Jane",
                last_name="Doe",
                phone_number="+447700900123",
            )
            user.is_verified = True
            user.save(update_fields=["is_verified"])
