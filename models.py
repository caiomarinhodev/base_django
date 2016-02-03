from __future__ import unicode_literals

from django.db import models

# Create your models here.
class BaseModel(models.Model):

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]


class SimpleBaseModel(BaseModel):
    name = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class ModifiableBaseModel(BaseModel):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class RemovableBaseModel(ModifiableBaseModel):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class FullBaseModel(BaseModel):
    name = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
