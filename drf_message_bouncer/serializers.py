from logging import getLogger
from decimal import Decimal

from rest_framework import serializers, exceptions

from .models import Message, Session


logger = getLogger('django')


class MessageSerializer(serializers.ModelSerializer):
    session = serializers.CharField(source="session.identifier")

    class Meta:
        model = Message
        fields = (
            'id',
            'session',
            'message',
            'original',
            'parent',
            'latitude',
            'longitude',
            'created',
            'updated',
        )
        read_only_fields = (
            'id',
            'session',
            'message',
            'original',
            'parent',
            'latitude',
            'longitude',
            'created',
            'updated',
        )


class CreateMessageSerializer(MessageSerializer):
    parent = serializers.CharField(required=False)
    session = serializers.CharField()

    class Meta:
        model = MessageSerializer.Meta.model
        fields = MessageSerializer.Meta.fields
        read_only_fields =  ('id', 'original',)

    def validate_latitude(self, latitude):
        if not Decimal(-90) <= Decimal(latitude) <= Decimal(90):
            raise serializers.ValidationError("Invalid latitude.")
        return latitude

    def validate_longitude(self, longitude):
        if not Decimal(-180) <= Decimal(longitude) <= Decimal(180):
            raise serializers.ValidationError("Invalid longitude.")
        return longitude

    def validate_session(self, session):
        try:
            return Session.objects.get(identifier=session)
        except Session.DoesNotExist:
            raise serializers.ValidationError("Invalid parent.")

    def validate_parent(self, parent):
        try:
            return Message.objects.get(id=parent)
        except Message.DoesNotExist:
            raise serializers.ValidationError("Invalid parent.")

    def validate(self, validated_data):
        session = validated_data.get("session")

        # Check if a parent is included.
        if  validated_data.get("parent"):
            # An original value is set on the parent.
            if validated_data["parent"].original:
                validated_data["original"] = validated_data["parent"].original
            # The parent is the original.
            else:
                validated_data["original"] = validated_data["parent"]

        if validated_data.get("parent") and Message.objects.filter(
                session=session, original=validated_data.get("original")).exists():
            raise serializers.ValidationError(
                {"parent": ["Cannot send the same message more than once."]}
            )

        return validated_data


class SessionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='identifier', read_only=True)
    class Meta:
        model = Session
        fields = (
            'id',
            'latitude',
            'longitude',
            'created',
            'updated',
        )
        read_only_fields = (
            'id',
            'latitude',
            'longitude',
            'created',
            'updated',
        )


class CreateSessionSerializer(SessionSerializer):

    class Meta:
        model = SessionSerializer.Meta.model
        fields = SessionSerializer.Meta.fields
        read_only_fields =  ('id', 'created', 'updated',)

    def validate_latitude(self, latitude):
        if not Decimal(-90) <= Decimal(latitude) <= Decimal(90):
            raise serializers.ValidationError("Invalid latitude.")
        return latitude

    def validate_longitude(self, longitude):
        if not Decimal(-180) <= Decimal(longitude) <= Decimal(180):
            raise serializers.ValidationError("Invalid longitude.")
        return longitude

    def create(self, validated_data):
        return Session.objects.create(**validated_data)
