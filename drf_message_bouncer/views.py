from logging import getLogger

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import exceptions

from .serializers import ExampleModelSerializer
from .models import ExampleModel


logger = getLogger('django')


class ListExampleModelView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ExampleModelSerializer

    def get_queryset(self):
        return ExampleModel.objects.all().order_by('created')


class RetrieveExampleModelView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ExampleModelSerializer

    def get_object(self):
        try:
            return ExampleModel.objects.get(id=self.kwargs['id'],)
        except ExampleModel.DoesNotExist:
            raise exceptions.NotFound()
