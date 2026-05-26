"""
Seed the database with demo data for Orel Fashion.
Run: python manage.py seed
"""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.catalog.models import Category, Color, Discount, Product, ProductVariant, Size
from apps.core.models import Branch, HeroContent, HomeFeatureCard

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with demo data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")
        self._seed_colors_sizes_categories()
        self._seed_hero()
        self._seed_home_feature_cards()
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
            ("Olive", "#556b2f"),
            ("Grey", "#808080"),
            ("Cream", "#fffdd0"),
            ("Chocolate", "#7b3f00"),
        ]

        for name, hex_code in colors:
            Color.objects.get_or_create(name=name, defaults={"hex_code": hex_code})

        sizes = [
            ("XS", 1),
            ("S", 2),
            ("M", 3),
            ("L", 4),
            ("XL", 5),
            ("XXL", 6),
        ]

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
        HeroContent.objects.update_or_create(
            title="Autumn / Winter 2026",
            defaults={
                "subtitle": "Refined essentials for the modern wardrobe",
                "cta_text": "Explore Collection",
                "cta_link": "/shop/new/",
                "is_active": True,
                "sort_order": 0,
            },
        )

    def _seed_home_feature_cards(self):
        HomeFeatureCard.objects.all().delete()

        cards = [
            {
                "label": "Orel Fashion",
                "title": "Men",
                "link": "/shop/men/",
                "sort_order": 0,
                "active": True,
            },
            {
                "label": "New Collection",
                "title": "Women",
                "link": "/shop/women/",
                "sort_order": 1,
                "active": True,
            },
            {
                "label": "Limited Offer",
                "title": "Kids",
                "link": "/shop/kids/",
                "sort_order": 2,
                "active": True,
            },
        ]

        for card in cards:
            HomeFeatureCard.objects.create(**card)

    def _seed_branches(self):
        Branch.objects.all().delete()

        branches = [
            {
                "name": "Orel Fashion Tehran Valiasr",
                "address": "Valiasr Street, No. 128",
                "city": "Tehran",
                "postcode": "19617",
                "country": "Iran",
                "phone": "+98 21 8876 2345",
                "email": "tehran@orelfashion.com",
                "opening_hours": "Sat–Thu 10:00–21:00",
                "latitude": Decimal("35.721858"),
                "longitude": Decimal("51.410341"),
                "google_maps_link": "https://maps.google.com/?q=35.721858,51.410341",
            },
            {
                "name": "Orel Fashion Tehran Jordan",
                "address": "Jordan Blvd, No. 55",
                "city": "Tehran",
                "postcode": "19158",
                "country": "Iran",
                "phone": "+98 21 2291 1020",
                "email": "jordan@orelfashion.com",
                "opening_hours": "Sat–Thu 10:00–22:00",
                "latitude": Decimal("35.760112"),
                "longitude": Decimal("51.412345"),
                "google_maps_link": "https://maps.google.com/?q=35.760112,51.412345",
            },
            {
                "name": "Orel Fashion Mashhad",
                "address": "Ahmadabad Street, No. 21",
                "city": "Mashhad",
                "postcode": "91856",
                "country": "Iran",
                "phone": "+98 51 3765 8821",
                "email": "mashhad@orelfashion.com",
                "opening_hours": "Everyday 10:00–22:00",
                "latitude": Decimal("36.297201"),
                "longitude": Decimal("59.606200"),
                "google_maps_link": "https://maps.google.com/?q=36.297201,59.606200",
            },
            {
                "name": "Orel Fashion Shiraz",
                "address": "Maali Abad Blvd, Corner 12",
                "city": "Shiraz",
                "postcode": "71987",
                "country": "Iran",
                "phone": "+98 71 3620 1180",
                "email": "shiraz@orelfashion.com",
                "opening_hours": "Everyday 10:00–21:30",
                "latitude": Decimal("29.615683"),
                "longitude": Decimal("52.485007"),
                "google_maps_link": "https://maps.google.com/?q=29.615683,52.485007",
            },
            {
                "name": "Orel Fashion Isfahan",
                "address": "Chaharbagh Abbasi, No. 88",
                "city": "Isfahan",
                "postcode": "81456",
                "country": "Iran",
                "phone": "+98 31 3224 5588",
                "email": "isfahan@orelfashion.com",
                "opening_hours": "Everyday 10:00–21:00",
                "latitude": Decimal("32.654627"),
                "longitude": Decimal("51.667983"),
                "google_maps_link": "https://maps.google.com/?q=32.654627,51.667983",
            },
            {
                "name": "Orel Fashion London Regent",
                "address": "42 Regent Street",
                "city": "London",
                "postcode": "W1B 5RA",
                "country": "United Kingdom",
                "phone": "+44 20 7946 0123",
                "email": "regent@orelfashion.com",
                "opening_hours": "Mon–Sat 10:00–20:00",
                "latitude": Decimal("51.510357"),
                "longitude": Decimal("-0.136439"),
                "google_maps_link": "https://maps.google.com/?q=51.510357,-0.136439",
            },
            {
                "name": "Orel Fashion London Kensington",
                "address": "15 Kensington High Street",
                "city": "London",
                "postcode": "W8 5NP",
                "country": "United Kingdom",
                "phone": "+44 20 7123 9988",
                "email": "kensington@orelfashion.com",
                "opening_hours": "Mon–Sun 10:00–20:00",
                "latitude": Decimal("51.501020"),
                "longitude": Decimal("-0.192840"),
                "google_maps_link": "https://maps.google.com/?q=51.501020,-0.192840",
            },
            {
                "name": "Orel Fashion Manchester",
                "address": "18 King Street",
                "city": "Manchester",
                "postcode": "M2 6AZ",
                "country": "United Kingdom",
                "phone": "+44 161 496 0456",
                "email": "manchester@orelfashion.com",
                "opening_hours": "Mon–Sat 10:00–19:00",
                "latitude": Decimal("53.480759"),
                "longitude": Decimal("-2.242631"),
                "google_maps_link": "https://maps.google.com/?q=53.480759,-2.242631",
            },
            {
                "name": "Orel Fashion Paris",
                "address": "12 Avenue Montaigne",
                "city": "Paris",
                "postcode": "75008",
                "country": "France",
                "phone": "+33 1 4256 8821",
                "email": "paris@orelfashion.com",
                "opening_hours": "Mon–Sat 10:00–20:00",
                "latitude": Decimal("48.866421"),
                "longitude": Decimal("2.303247"),
                "google_maps_link": "https://maps.google.com/?q=48.866421,2.303247",
            },
            {
                "name": "Orel Fashion Milan",
                "address": "Via Monte Napoleone 8",
                "city": "Milan",
                "postcode": "20121",
                "country": "Italy",
                "phone": "+39 02 8821 9988",
                "email": "milan@orelfashion.com",
                "opening_hours": "Mon–Sat 10:00–20:00",
                "latitude": Decimal("45.468503"),
                "longitude": Decimal("9.195560"),
                "google_maps_link": "https://maps.google.com/?q=45.468503,9.195560",
            },
        ]

        for index, data in enumerate(branches):
            Branch.objects.create(
                sort_order=index,
                active=True,
                **data,
            )

    def _seed_products(self):
        self.stdout.write("Resetting demo products...")

        Discount.objects.all().delete()
        ProductVariant.objects.all().delete()
        Product.objects.all().delete()

        men_categories = list(Category.objects.filter(section=Category.Section.MEN))
        women_categories = list(Category.objects.filter(section=Category.Section.WOMEN))
        kids_categories = list(Category.objects.filter(section=Category.Section.KIDS))

        colors = list(Color.objects.all().order_by("name"))
        sizes = list(Size.objects.all().order_by("sort_order"))

        men_models = [
            ("Wool Coat", "A structured men wool coat with premium lining.", Decimal("189.00")),
            ("Cotton Shirt", "A breathable men cotton shirt for everyday styling.", Decimal("49.00")),
            ("Tailored Trousers", "Modern men tailored trousers with a clean fit.", Decimal("79.00")),
            ("Knit Jumper", "Soft men knit jumper for colder seasons.", Decimal("89.00")),
            ("Denim Jacket", "Classic men denim jacket with durable stitching.", Decimal("99.00")),
            ("Blazer", "Minimal men blazer with polished tailoring.", Decimal("159.00")),
            ("Puffer Jacket", "Lightweight men puffer jacket with insulated warmth.", Decimal("129.00")),
            ("Linen Shirt", "Light men linen shirt for warm days.", Decimal("59.00")),
            ("Slim Fit Jeans", "Everyday men slim fit jeans with a modern cut.", Decimal("74.00")),
            ("Overshirt", "Layered men overshirt with a structured finish.", Decimal("84.00")),
        ]

        women_models = [
            ("Wool Coat", "A structured women wool coat with premium lining.", Decimal("199.00")),
            ("Satin Dress", "Elegant women satin dress with a smooth drape.", Decimal("119.00")),
            ("Knit Jumper", "Soft women knit jumper for colder seasons.", Decimal("79.00")),
            ("Wide Leg Jeans", "Comfortable women wide leg jeans.", Decimal("74.00")),
            ("Blazer", "Minimal women blazer with polished tailoring.", Decimal("149.00")),
            ("Draped Blouse", "Soft women draped blouse with a refined shape.", Decimal("69.00")),
            ("Puffer Jacket", "Lightweight women puffer jacket with insulated warmth.", Decimal("129.00")),
            ("Linen Top", "Light women linen top for warm days.", Decimal("39.00")),
            ("Midi Skirt", "Elegant women midi skirt with a soft drape.", Decimal("64.00")),
            ("Trench Coat", "Classic women trench coat with a timeless finish.", Decimal("179.00")),
        ]

        kids_models = [
            ("Wool Coat", "Warm kids wool coat with soft lining.", Decimal("89.00")),
            ("Cotton Shirt", "Breathable kids cotton shirt for everyday outfits.", Decimal("29.00")),
            ("Trousers", "Comfortable kids trousers with durable stitching.", Decimal("34.00")),
            ("Knit Jumper", "Soft kids knit jumper for warmth and comfort.", Decimal("39.00")),
            ("Denim Jacket", "Classic kids denim jacket with relaxed styling.", Decimal("49.00")),
            ("Puffer Jacket", "Lightweight kids puffer jacket with insulated warmth.", Decimal("69.00")),
            ("Linen Top", "Light kids linen top for warm days.", Decimal("24.00")),
            ("Jeans", "Durable kids jeans with a comfortable fit.", Decimal("36.00")),
            ("Hoodie", "Soft kids hoodie with a cozy fit.", Decimal("42.00")),
            ("Dress", "Comfortable kids dress with a polished look.", Decimal("44.00")),
        ]

        gender_configs = [
            ("women", "Women", women_categories, women_models, 50),
            ("men", "Men", men_categories, men_models, 50),
            ("kids", "Kids", kids_categories, kids_models, 50),
        ]

        now = timezone.now()
        total_products = 0
        total_variants = 0
        total_sales = 0

        for gender, prefix, category_pool, model_list, product_total in gender_configs:
            if not category_pool:
                self.stdout.write(self.style.WARNING(f"No category found for {prefix}. Skipping."))
                continue

            gender_sale_count = 0

            for i in range(1, product_total + 1):
                total_products += 1

                model_name, description, base_price = model_list[(i - 1) % len(model_list)]
                category = category_pool[(i - 1) % len(category_pool)]

                product = Product.objects.create(
                    title=f"{prefix} {model_name} {i:03d}",
                    description=(
                        f"{description} Demo item for testing filters by gender, "
                        f"color, size, price, newest, lowest price, highest price, and sale."
                    ),
                    category=category,
                    gender=gender,
                    is_new_arrival=i <= 15,
                    is_active=True,
                )

                for color_index, color in enumerate(colors):
                    for size_index, size in enumerate(sizes):
                        price = (
                            base_price
                            + Decimal(i % 12) * Decimal("3.00")
                            + Decimal(color_index * 2)
                            + Decimal(size_index * 4)
                        )

                        ProductVariant.objects.create(
                            product=product,
                            color=color,
                            size=size,
                            price=price,
                            stock=5 + ((i + color_index + size_index) % 25),
                            is_active=True,
                        )
                        total_variants += 1

                if i <= 4 or i % 10 == 0:
                    Discount.objects.create(
                        product=product,
                        percentage=15 + ((i % 3) * 5),
                        starts_at=now - timedelta(hours=2),
                        ends_at=now + timedelta(days=7),
                        label="Limited time deal",
                        is_active=True,
                    )
                    gender_sale_count += 1
                    total_sales += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"{prefix}: created {product_total} products, all colors, all sizes, {gender_sale_count} sales."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {total_products} products, {total_variants} variants, {total_sales} sale deals."
            )
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