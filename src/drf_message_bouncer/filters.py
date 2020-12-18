from django_filters import rest_framework as filters

from drf_message_bouncer.models import Message


TRUE_VALUES = ('true', 'True', True)
FALSE_VALUES = ('false', 'False', False)


class MessageFilterSet(filters.FilterSet):
    broadcasted = filters.CharFilter(method='filter_broadcasted')

    class Meta:
        model = Message
        fields = {
            'id': ['exact',],
        }

    def broadcasted(self, queryset, name, value):
        if value in TRUE_VALUES:
            pass
            # queryset.filter(
            #     message__parent_children__session=self.request.session
            # )
        elif value in FALSE_VALUES:
            queryset.exclude(
                message__parent_children__session=self.request.session
            )

        return queryset
