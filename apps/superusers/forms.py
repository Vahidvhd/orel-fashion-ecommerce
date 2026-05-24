from django import forms

from apps.core.models import HeroContent


class HeroContentForm(forms.ModelForm):
    class Meta:
        model = HeroContent
        fields = [
            "title",
            "subtitle",
            "hero_image",
            "hero_video",
            "cta_text",
            "cta_link",
            "is_active",
        ]