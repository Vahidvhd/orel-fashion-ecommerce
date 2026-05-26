from django import forms

from apps.core.models import (
    Branch,
    BusinessSettings,
    HeroContent,
    HomeFeatureCard,
    HomeMediaSection,
)


INPUT_CLASS = "w-full rounded-md border border-neutral-300 px-3 py-2 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black"
CHECKBOX_CLASS = "h-4 w-4 rounded border-neutral-300 text-black focus:ring-black"


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
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "subtitle": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "cta_text": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "cta_link": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "is_active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASS}),
        }


class HomeFeatureCardForm(forms.ModelForm):
    class Meta:
        model = HomeFeatureCard
        fields = [
            "label",
            "title",
            "image",
            "link",
            "active",
            "sort_order",
        ]
        widgets = {
            "label": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "title": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "link": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "sort_order": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASS}),
        }


class HomeMediaSectionForm(forms.ModelForm):
    class Meta:
        model = HomeMediaSection
        fields = [
            "title",
            "subtitle",
            "image_1",
            "image_2",
            "image_3",
            "image_4",
            "video",
            "video_poster",
            "active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "subtitle": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASS}),
        }


class BusinessSettingsForm(forms.ModelForm):
    class Meta:
        model = BusinessSettings
        fields = ["store_type"]
        widgets = {
            "store_type": forms.Select(attrs={"class": INPUT_CLASS}),
        }


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = [
            "name",
            "address",
            "city",
            "postcode",
            "country",
            "phone",
            "email",
            "opening_hours",
            "latitude",
            "longitude",
            "google_maps_link",
            "active",
            "sort_order",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "required": True}),
            "address": forms.TextInput(attrs={"class": INPUT_CLASS, "required": True}),
            "city": forms.TextInput(attrs={"class": INPUT_CLASS, "required": True}),
            "postcode": forms.TextInput(attrs={"class": INPUT_CLASS, "required": True}),
            "country": forms.TextInput(attrs={"class": INPUT_CLASS, "required": True}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASS, "required": True}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "required": True}),
            "opening_hours": forms.TextInput(attrs={"class": INPUT_CLASS, "required": True}),
            "latitude": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "any", "required": True}),
            "longitude": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "any", "required": True}),
            "google_maps_link": forms.URLInput(attrs={"class": INPUT_CLASS, "required": True}),
            "sort_order": forms.NumberInput(attrs={"class": INPUT_CLASS, "required": True}),
            "active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASS}),
        }