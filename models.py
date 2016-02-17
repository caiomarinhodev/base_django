from __future__ import unicode_literals

from django.db import models, IntegrityError
from django.utils.text import slugify
from utils import utils
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


class FullSlugBaseModel(BaseModel):
    name = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
            try:
                return super(FullSlugBaseModel, self).save(force_insert, force_update, using, update_fields)
            except IntegrityError:
                self.slug = self.slug + "-" + utils.generate_random_string(4)
        return super(FullSlugBaseModel, self).save(force_insert, force_update, using, update_fields)
