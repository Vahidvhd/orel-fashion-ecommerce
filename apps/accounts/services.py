import random
import string
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from apps.accounts.models import User, VerificationCode


def generate_verification_code(length=None) -> str:
    length = length or settings.VERIFICATION_CODE_LENGTH
    return "".join(random.choices(string.digits, k=length))


def create_verification_code(user: User, channel: str = VerificationCode.Channel.EMAIL) -> VerificationCode:
    VerificationCode.objects.filter(user=user, is_used=False).update(is_used=True)
    code = generate_verification_code()
    expires_at = timezone.now() + timedelta(minutes=settings.VERIFICATION_CODE_EXPIRY_MINUTES)
    verification = VerificationCode.objects.create(
        user=user,
        code=code,
        channel=channel,
        expires_at=expires_at,
    )
    send_verification_code(user, code, channel)
    return verification


def send_verification_code(user: User, code: str, channel: str) -> None:
    if channel == VerificationCode.Channel.SMS:
        send_sms_verification(user.phone_number, code)
    else:
        send_email_verification(user.email, code)


def send_email_verification(email: str, code: str) -> None:
    from django.core.mail import send_mail

    send_mail(
        subject="Verify your Orel Fashion account",
        message=f"Your verification code is: {code}\n\nThis code expires in "
        f"{settings.VERIFICATION_CODE_EXPIRY_MINUTES} minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def send_sms_verification(phone: str, code: str) -> None:
    backend = getattr(settings, "SMS_BACKEND", "console")
    if backend == "console":
        print(f"[SMS] To {phone}: Your verification code is {code}")  # noqa: T201
    # Extend with Twilio etc. in production


def verify_code(user: User, code: str) -> bool:
    verification = (
        VerificationCode.objects.filter(user=user, code=code, is_used=False)
        .order_by("-created_at")
        .first()
    )
    if not verification or not verification.is_valid:
        return False
    verification.is_used = True
    verification.save(update_fields=["is_used"])
    user.is_verified = True
    user.verified_at = timezone.now()
    user.save(update_fields=["is_verified", "verified_at"])
    return True
