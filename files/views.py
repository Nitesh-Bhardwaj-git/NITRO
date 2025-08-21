import csv
import io
import threading
from typing import Any, Dict, List

from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from .models import UploadedFile


def _parse_file_async(uploaded_file_id: int) -> None:
    try:
        file_record = UploadedFile.objects.get(id=uploaded_file_id)
        file_record.status = UploadedFile.Status.PROCESSING
        file_record.progress = 5
        file_record.save(update_fields=['status', 'progress'])

        # Read file content
        file_record.progress = 20
        file_record.save(update_fields=['progress'])
        with file_record.file.open('rb') as f:
            raw = f.read()

        # Detect CSV and parse
        file_record.progress = 40
        file_record.save(update_fields=['progress'])
        try:
            text = raw.decode('utf-8')
        except Exception:
            text = raw.decode('latin-1')

        data: List[Dict[str, Any]]
        csv_stream = io.StringIO(text)
        reader = csv.DictReader(csv_stream)
        data = [row for row in reader]

        file_record.progress = 90
        file_record.parsed_content = data
        file_record.status = UploadedFile.Status.READY
        file_record.progress = 100
        file_record.save(update_fields=['parsed_content', 'status', 'progress'])
    except Exception:
        UploadedFile.objects.filter(id=uploaded_file_id).update(status=UploadedFile.Status.FAILED)


@csrf_exempt
def files_collection(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'detail': 'Missing file'}, status=400)

        django_file = request.FILES['file']
        with transaction.atomic():
            record = UploadedFile.objects.create(
                file=django_file,
                filename=django_file.name,
                status=UploadedFile.Status.UPLOADING,
                progress=0,
            )

        # Start background parsing thread
        t = threading.Thread(target=_parse_file_async, args=(record.id,), daemon=True)
        t.start()
        return JsonResponse({'file_id': record.id, 'status': record.status, 'progress': record.progress})
    elif request.method == 'GET':
        records = UploadedFile.objects.order_by('-created_at').values('id', 'filename', 'status', 'created_at')
        return JsonResponse({'files': list(records)})
    else:
        return JsonResponse({'detail': 'Method Not Allowed'}, status=405)


def get_progress(request: HttpRequest, file_id) -> JsonResponse:
    record = get_object_or_404(UploadedFile, id=file_id)
    return JsonResponse({'file_id': record.id, 'status': record.status, 'progress': record.progress})


def file_resource(request: HttpRequest, file_id) -> JsonResponse:
    record = get_object_or_404(UploadedFile, id=file_id)
    if request.method == 'GET':
        if record.status != UploadedFile.Status.READY:
            return JsonResponse({'message': 'File upload or processing in progress. Please try again later.'}, status=202)
        return JsonResponse({'file_id': record.id, 'status': record.status, 'content': record.parsed_content})
    elif request.method == 'DELETE':
        record.delete()
        return JsonResponse({'deleted': True})
    else:
        return JsonResponse({'detail': 'Method Not Allowed'}, status=405)


def list_files(request: HttpRequest) -> JsonResponse:
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method Not Allowed'}, status=405)
    records = UploadedFile.objects.order_by('-created_at').values('id', 'filename', 'status', 'created_at')
    return JsonResponse({'files': list(records)})


@csrf_exempt
def delete_file(request: HttpRequest, file_id) -> JsonResponse:
    if request.method not in ('DELETE', 'POST'):
        return JsonResponse({'detail': 'Method Not Allowed'}, status=405)
    record = get_object_or_404(UploadedFile, id=file_id)
    record.delete()
    return JsonResponse({'deleted': True})

