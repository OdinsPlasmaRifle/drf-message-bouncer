from logging import getLogger

from django.db import models


logger = getLogger('django')


class ExampleModel(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

