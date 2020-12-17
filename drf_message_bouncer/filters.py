from django_filters import rest_framework as filters

from drf_message_bouncer.models import Message


class MessageFilterSet(filters.FilterSet):

    class Meta:
        model = Message
        fields = {
            'id': ['exact',],
        }
