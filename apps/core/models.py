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


class Branch(models.Model):
    name = models.CharField(max_length=150)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="United Kingdom")
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_embed_url = models.URLField(
        blank=True,
        help_text="Google Maps embed URL or static map link",
    )
    opening_hours = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "branches"

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        parts = [self.address_line1, self.address_line2, self.city, self.postcode, self.country]
        return ", ".join(p for p in parts if p)
