from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_booking_mail(username: str):
    send_mail(
        f"Hello {username}",
        "you succesfully booked a house",
        "info@farm.com",
        [username]
    )
