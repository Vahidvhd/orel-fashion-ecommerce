from urllib.parse import quote_plus

from django.core.exceptions import ValidationError
from django.db import models


class HeroContent(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to="hero/", blank=True, null=True)
    hero_video = models.FileField(upload_to="hero/videos/", blank=True, null=True)
    cta_text = models.CharField(max_length=100, blank=True)
    cta_link = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name_plural = "hero content"

    def __str__(self):
        return self.title

    @property
    def has_video(self):
        return bool(self.hero_video)

    @property
    def has_image(self):
        return bool(self.hero_image)


class HomeFeatureCard(models.Model):
    label = models.CharField(max_length=80)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="home/cards/", blank=True, null=True)
    link = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "home feature card"
        verbose_name_plural = "home feature cards"

    def __str__(self):
        return self.title

    def clean(self):
        if self.active:
            active_cards = HomeFeatureCard.objects.filter(active=True)

            if self.pk:
                active_cards = active_cards.exclude(pk=self.pk)

            if active_cards.count() >= 4:
                raise ValidationError("You can only have up to 4 active home feature cards.")


class HomeMediaSection(models.Model):
    title = models.CharField(max_length=150, default="This Is OREL")
    subtitle = models.CharField(max_length=255, blank=True)
    image_1 = models.ImageField(upload_to="home/media/", blank=True, null=True)
    image_2 = models.ImageField(upload_to="home/media/", blank=True, null=True)
    image_3 = models.ImageField(upload_to="home/media/", blank=True, null=True)
    image_4 = models.ImageField(upload_to="home/media/", blank=True, null=True)
    video = models.FileField(upload_to="home/media/videos/", blank=True, null=True)
    video_poster = models.ImageField(upload_to="home/media/posters/", blank=True, null=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "home media section"
        verbose_name_plural = "home media section"

    def __str__(self):
        return self.title

    @classmethod
    def get_active(cls):
        return cls.objects.filter(active=True).first()

    @property
    def images(self):
        return [
            image
            for image in [self.image_1, self.image_2, self.image_3, self.image_4]
            if image
        ]


class BusinessSettings(models.Model):
    ONLINE_ONLY = "online"
    PHYSICAL_STORE = "physical"

    STORE_TYPE_CHOICES = [
        (ONLINE_ONLY, "Online shop only"),
        (PHYSICAL_STORE, "Physical store"),
    ]

    store_type = models.CharField(
        max_length=20,
        choices=STORE_TYPE_CHOICES,
        default=ONLINE_ONLY,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "business settings"
        verbose_name_plural = "business settings"

    def __str__(self):
        return self.get_store_type_display()

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def is_online_only(self):
        return self.store_type == self.ONLINE_ONLY

    @property
    def is_physical_store(self):
        return self.store_type == self.PHYSICAL_STORE


class Branch(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="United Kingdom")
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    google_maps_link = models.URLField()
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "branches"

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        parts = [self.address, self.city, self.postcode, self.country]
        return ", ".join(p for p in parts if p)

    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None

    @property
    def map_embed_url(self):
        if self.has_coordinates:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}&output=embed"

        if self.full_address:
            return f"https://www.google.com/maps?q={quote_plus(self.full_address)}&output=embed"

        return ""

    @property
    def open_in_google_maps_url(self):
        if self.google_maps_link:
            return self.google_maps_link

        if self.has_coordinates:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"

        if self.full_address:
            return f"https://www.google.com/maps/search/?api=1&query={quote_plus(self.full_address)}"

        return ""