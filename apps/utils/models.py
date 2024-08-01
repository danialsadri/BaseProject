import uuid
from django.db import models
from django.http import Http404


def image_upload_to(instance, filename):
    return f'public_html/images/image_{instance.id}.{filename.split(".")[-1]}'


def file_upload_to(instance, filename):
    return f'public_html/files/files_{instance.id}.{filename.split(".")[-1]}'


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True, verbose_name='آیدی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='ویرایش شده در')

    class Meta:
        abstract = True

    def update(self, **kwargs):
        for field in kwargs:
            self.__setattr__(field, kwargs[field])
        self.save()

    @classmethod
    def get_object_or_404(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            raise Http404

    @classmethod
    def is_exist(cls, *args, **kwargs):
        obj = cls.objects.filter(*args, **kwargs)
        return obj.exists(), obj.first()


class ImageModel(BaseModel):
    image = models.ImageField(upload_to=image_upload_to, verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        return self.image.name
