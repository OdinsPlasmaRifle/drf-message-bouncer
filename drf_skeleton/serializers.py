from logging import getLogger

from rest_framework import serializers, exceptions

from .models import ExampleModel


logger = getLogger('django')


class ExampleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExampleModel
        fields = ('id', 'created', 'updated',)
