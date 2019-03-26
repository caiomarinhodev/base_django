from django.db.models import (
    TextField,
    IntegerField,
    EmailField
)
from django.forms.widgets import (
    Textarea,
    NumberInput,
    EmailInput,
    Input
)

import random
import string
import csv


def generate_random_string(n):
    """
    Generates a random string of length n
    :param n: Length of string
    :return: Random string
    """
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    """
    CSV reader for UTF-8 documents
    :param unicode_csv_data: Data of CSV
    :param dialect: Dialect of CSV
    :param kwargs: Other args
    :return:
    """
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [str(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    """
    UTF-8 Encoder
    :param unicode_csv_data:
    :return: Generator of UTF-8 encoding
    """
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def field_to_widget(field):
    if type(field) is TextField:
        return Textarea(attrs={"class": "form-control", "rows": 1})
    if type(field) is IntegerField:
        return NumberInput(attrs={"class": "form-control"})
    if type(field) is EmailField:
        return EmailInput(attrs={"class": "form-control"})
    return Input(attrs={"class": "form-control"})


def generate_bootstrap_widgets_for_all_fields(model):
    return {x.name: field_to_widget(x) for x in model._meta.fields}
