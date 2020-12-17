from logging import getLogger

from rest_framework import status
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *
from .filters import *


logger = getLogger('django')


class ListCreateMessageView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MessageFilterSet

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateMessageSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        try:
            session = Session.objects.get(identifier=self.request.GET.get("session"))
        except Session.DoesNotExist:
            raise exceptions.PermissionDenied

        message_ids = Message.objects.in_range(session.latitude, session.longitude, 5000)

        return Message.objects.filter(
            Q(session=session) | Q(id__in=message_ids)
        ).order_by('created')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            self.serializer_class(
                serializer.instance, context=self.get_serializer_context()
            ).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class RetrieveMessageView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MessageSerializer

    def get_object(self):
        try:
            return Message.objects.get(id=self.kwargs['id'],)
        except Message.DoesNotExist:
            raise exceptions.NotFound()


class CreateSessionView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateSessionSerializer

