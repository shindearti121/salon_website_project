"""Booking views for creating appointments.

This module provides a simple, validated view to create
`Appointment` instances and notify the salon by email.
"""

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import AppointmentForm

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def book_appointment(request):
    """
    Display and handle the appointment booking form.

    Uses `AppointmentForm` for validation. On successful POST the appointment
    is saved and a notification email is sent to the salon. Email failures
    are logged but do not prevent the booking.
    """
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()

            # Build email values safely from possible field names
            name = getattr(appointment, "name", None) or getattr(appointment, "customer_name", "Unknown")
            phone = getattr(appointment, "phone", "N/A")
            service = getattr(appointment, "service", "N/A")
            date = getattr(appointment, "date", "N/A")
            time = getattr(appointment, "time", None)

            subject = f"New Appointment: {name}"
            message_lines = [
                f"Name: {name}",
                f"Phone: {phone}",
                f"Service: {service}",
                f"Date: {date}",
            ]
            if time:
                message_lines.append(f"Time: {time}")
            message = "\n".join(message_lines)

            salon_email = getattr(settings, "SALON_EMAIL", None) or getattr(settings, "DEFAULT_FROM_EMAIL", None)
            if not salon_email:
                salon_email = "salon@example.com"

            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", salon_email)

            try:
                send_mail(subject, message, from_email, [salon_email])
            except Exception:
                logger.exception("Failed to send appointment notification email")

            return redirect("success")
    else:
        form = AppointmentForm()

    return render(request, "booking.html", {"form": form})


def success(request):
    return render(request, "success.html")
