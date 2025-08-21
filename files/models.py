import uuid
from django.db import models


class UploadedFile(models.Model):
    class Status(models.TextChoices):
        UPLOADING = 'uploading'
        PROCESSING = 'processing'
        READY = 'ready'
        FAILED = 'failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADING)
    progress = models.PositiveSmallIntegerField(default=0)
    # Store parsed content as JSON for simplicity
    parsed_content = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id}:{self.filename}:{self.status}:{self.progress}%"

