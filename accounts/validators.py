import os
from django.core.exceptions import ValidationError


def allow_only_images(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.jpg','.png','.pjeg']
    if not ext.low() in valid_extensions:
        raise ValidationError("Image extension is not valid, valid extensions are '.jpg','.png','.pjeg' ")