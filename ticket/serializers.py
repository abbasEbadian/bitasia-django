from rest_framework import serializers

from ticket.models import Ticket, TicketMessage
from users.serializer import UserSimplifiedSerializer


class TicketMessageSerializer(serializers.ModelSerializer):
    user_id = UserSimplifiedSerializer()

    class Meta:
        model = TicketMessage
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_admin'] = instance.user_id.is_staff
        return ret


class TicketCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    department = serializers.ChoiceField(required=True, choices=Ticket.Department.choices)

    def create(self, validated_data):
        instance = Ticket.objects.create(**{
            "user_id": validated_data["user_id"],
            "title": validated_data["title"],
            "department": validated_data["department"]
        })
        instance.messages.create(**{
            "message": validated_data["message"],
            "user_id": validated_data["user_id"],
        })
        instance.save()
        return instance


class TicketSerializer(serializers.ModelSerializer):
    user_id = UserSimplifiedSerializer()
    messages = TicketMessageSerializer(many=True)

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketAddMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        user = validated_data["user_id"]
        instance.messages.create(**{
            "message": validated_data["message"],
            "user_id": user,
        })
        instance.status = Ticket.Status.ANSWERED if validated_data["is_moderator"] else Ticket.Status.PENDING
        instance.save()
        return instance
