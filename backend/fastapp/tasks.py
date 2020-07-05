 from .celery import app
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from service.models import Service
User = get_user_model()

@app.task
def send_service_contact_mail(user_id, service_id):
    user = User.objects.get(pk=user_id)
    service = Service.objects.get(pk=service_id)
    send_mail(
        'Subject here',
        'Here is the message.',
        user.username,
        [service.user.username],
        fail_silently=False,
    )
