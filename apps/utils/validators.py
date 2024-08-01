import os
import re
from io import BytesIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from config.error_manager import ErrorHandler


def get_image_instance(image):
    # Uploaded file is in memory
    if isinstance(image, InMemoryUploadedFile):
        memory_image = BytesIO(image.read())
        pil_image = PilImage.open(memory_image)
        img_format = os.path.splitext(image.name)[1][1:].upper()
        img_format = 'JPEG' if img_format == 'JPG' else img_format
        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)
        new_image = ContentFile(new_image.getvalue())
        return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)
    # Uploaded file is in disk
    elif isinstance(image, TemporaryUploadedFile):
        path = image.temporary_file_path()
        pil_image = PilImage.open(path)
        pil_image.save(path)
        image.size = os.stat(path).st_size
    return image


def validate_phone(value):
    phone_regex = re.compile(r'^(09)+?\d{9}', re.IGNORECASE)
    validate = [phone_regex.fullmatch(value)]
    if not any(validate):
        raise ErrorHandler.get_error_exception(400, "invalid_phone")


def validate_otp_code(value):
    if len(str(value)) != 4:
        raise ErrorHandler.get_error_exception(400, "invalid_otp_code")
