from celery import shared_task

from apps.accounts.models import User
from apps.accounts.services import create_verification_code


@shared_task
def send_verification_code_task(user_id: int, channel: str = "email"):
    user = User.objects.get(pk=user_id)
    create_verification_code(user, channel=channel)
