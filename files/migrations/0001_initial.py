import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('filename', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('uploading', 'uploading'), ('processing', 'processing'), ('ready', 'ready'), ('failed', 'failed')], default='uploading', max_length=20)),
                ('progress', models.PositiveSmallIntegerField(default=0)),
                ('parsed_content', models.JSONField(null=True, blank=True)),
            ],
        ),
    ]


