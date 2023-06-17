from django.db import models


class ErrorLog(models.Model):
    """
    Model class for storing error logs.
    """
    message = models.CharField(max_length=255, help_text="Error message")
    stack_trace = models.TextField(help_text="Stack Trace")
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
    filename = models.CharField(max_length=255, default='firmware_upload_file')
    firmware_file = models.FileField(upload_to='firmwares/')
    chunk_size = models.IntegerField()
    checked_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.filename} ({self.checked_date.strftime('%d %b %Y %H:%M:%S')})"
