import random

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from apps.accounts.models import User
from apps.accounts.services import create_verification_code, verify_code


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=150, label="First name", required=True)
    surname = forms.CharField(max_length=150, label="Last name", required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=4,
        required=True,
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=True,
    )

    captcha = forms.CharField(label="Security check", required=True)

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["captcha"].help_text = "What is 1 + 8?"

    def clean_captcha(self):
        answer = self.cleaned_data.get("captcha", "").strip()
        if answer != "9":
            raise ValidationError("Incorrect answer. Please try again.")
        return answer

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data["email"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["name"],
            last_name=self.cleaned_data["surname"],
            phone_number=self.cleaned_data["phone_number"],
            is_active=True,
            is_verified=False,
        )
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            create_verification_code(user)

        return user

class VerificationForm(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(max_length=10, min_length=4)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")

        if not email:
            return cleaned

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("No account found with this email.")

        user.is_verified = True
        user.save(update_fields=["is_verified"])

        cleaned["user"] = user
        return cleaned


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("username", "").lower()
        password = self.cleaned_data.get("password")
        self.user_cache = authenticate(self.request, username=email, password=password)
        if self.user_cache is None:
            raise ValidationError("Invalid email or password.")
        if not self.user_cache.is_verified:
            raise ValidationError("Please verify your email before logging in.")
        return self.cleaned_data
