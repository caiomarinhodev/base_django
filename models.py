from __future__ import unicode_literals

from django.db import models, IntegrityError
from django.utils.text import slugify

from . import (
    utils,
    conf
)
# Create your models here.


class BaseModel(models.Model):
    """
    Default base models
    """

    visible_fields = None

    class Meta:
        abstract = True

    def display_fields(self):
        if self.visible_fields is not None:
            return (x for x in self._meta.fields if x.name in self.visible_fields)
        else:
            return self._meta.fields

    def get_fields(self):
        """
        Iterates over the model and return all fields and values
        :return: Array of tuples. Each tuple is (parameter, value of parameter)
        """
        return [(field.name, field.value_to_string(self)) for field in self.display_fields()]


class SimpleBaseModel(BaseModel):
    """
    Simple model model, includes a name and description
    """
    name = models.CharField(max_length=100, blank=True, verbose_name=conf.BASE_MODELS_TRANSLATION_NAME)
    description = models.TextField(blank=True, verbose_name=conf.BASE_MODELS_TRANSLATION_DESCRIPTION)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ModifiableBaseModel(BaseModel):
    """
    Simple base model to timestamp fields, created and modified included
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name=conf.BASE_MODELS_TRANSLATION_CREATED)
    modified = models.DateTimeField(auto_now=True, verbose_name=conf.BASE_MODELS_TRANSLATION_MODIFIED)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created)


class RemovableBaseModel(ModifiableBaseModel):
    """
    Simple base model, to check active objects, include an active flag
    """
    active = models.BooleanField(default=True, verbose_name=conf.BASE_MODELS_TRANSLATION_ACTIVE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class FullBaseModel(BaseModel):
    """
    Complete model, includes a mixin for SimpleBaseModel, ModifiableBaseModel and RemovableBaseModel
    """
    name = models.CharField(max_length=100, blank=True, verbose_name=conf.BASE_MODELS_TRANSLATION_NAME)
    description = models.TextField(blank=True, verbose_name=conf.BASE_MODELS_TRANSLATION_DESCRIPTION)
    created = models.DateTimeField(auto_now_add=True, verbose_name=conf.BASE_MODELS_TRANSLATION_CREATED)
    modified = models.DateTimeField(auto_now=True, verbose_name=conf.BASE_MODELS_TRANSLATION_MODIFIED)
    active = models.BooleanField(default=True, verbose_name=conf.BASE_MODELS_TRANSLATION_ACTIVE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class FullSlugBaseModel(BaseModel):
    """
    Complete model, includes the same from FullBaseModel and a slug field, to reference in URL in Class Based Views
    """
    name = models.CharField(max_length=100, blank=True, verbose_name=conf.BASE_MODELS_TRANSLATION_NAME)
    description = models.TextField(blank=True, verbose_name=conf.BASE_MODELS_TRANSLATION_DESCRIPTION)
    slug = models.SlugField(blank=True, unique=True, verbose_name=conf.BASE_MODELS_TRANSLATION_SLUG)
    created = models.DateTimeField(auto_now_add=True, verbose_name=conf.BASE_MODELS_TRANSLATION_CREATED)
    modified = models.DateTimeField(auto_now=True, verbose_name=conf.BASE_MODELS_TRANSLATION_MODIFIED)
    active = models.BooleanField(default=True, verbose_name=conf.BASE_MODELS_TRANSLATION_ACTIVE)
    SLUG_RANDOM_CHARS = 20
    MAX_RANDOM_TRIES = 5

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Custom save method, it checks if slug is unique and define a valid unique slug
        :param force_insert:  Might force the insert
        :param force_update: Might force the update
        :param using: Object using
        :param update_fields: Fields to be updated
        :return: Object
        """
        if not self.slug:
            self.slug = slugify(self.name)
        successful_save = False
        saved_object = None
        index_iterations = 0
        while not successful_save and index_iterations < self.MAX_RANDOM_TRIES:
            index_iterations += 1
            try:
                saved_object = super(FullSlugBaseModel, self).save(force_insert, force_update, using, update_fields)
                successful_save = True
            except IntegrityError as e:
                if len(self.slug)+self.SLUG_RANDOM_CHARS > 150:
                    self.slug = self.slug[:-self.SLUG_RANDOM_CHARS] + "-" + utils.generate_random_string(self.SLUG_RANDOM_CHARS)
                else:
                    self.slug = self.slug + "-" + utils.generate_random_string(self.SLUG_RANDOM_CHARS)

                if index_iterations == self.MAX_RANDOM_TRIES:
                    raise e
        return saved_object

    def __str__(self):
        return self.name
