from django.db import models
from django.conf import settings

filename = settings.FILENAME


class ErrorLog(models.Model):
    """
    Model class for storing error logs.
    """
    value = models.TextField(max_length=500, help_text="Error values", default="Error value")
    created = models.DateTimeField(auto_now_add=True, help_text="Time at which the error occurred")

    def __str__(self):
        return f"{self.message} ({self.created.strftime('%d %b %Y %H:%M:%S')})"


class UpdateCheck(models.Model):
    """
    Model class for checking updates.
    """
    version = models.CharField(max_length=10)
    checked_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default="status")

    def __str__(self):
        return f"{self.version} ({self.checked_date.strftime('%d %b %Y %H:%M:%S')})"


class Firmware(models.Model):
    """
    Model class for firmware updates.
    """
    filename = models.CharField(max_length=255, default=filename)
    firmware_file = models.FileField(upload_to='binfiles/')
    checked_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.filename} ({self.checked_date.strftime('%d %b %Y %H:%M:%S')})"
