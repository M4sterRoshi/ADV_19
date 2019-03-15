from rest_framework import serializers
from .models import Event, Registration, Coordinator
from user.models import User
from django.contrib.auth import authenticate

class EventListSerializer(serializers.ModelSerializer):
    tag_set = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    organizer = serializers.SlugRelatedField(read_only=True, slug_field='logo')
    class Meta:
        model = Event
        fields = ('name', 'code', 'tag_set', 'organizer')

class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventRegistrationSerializer(serializers.Serializer):
    user  = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    is_active = serializers.BooleanField(read_only=True)

    def validate(self, data):
        user = data.get('user', None)
        event = data.get('event', None)

        if user is None:
            raise serializers.ValidationError(
                'User not found'
            )

        if event is None:
            raise serializers.ValidationError(
                'A valid event id is required'
            )
        
        return {
            'user' : user,
            'event': event
        }

    def create(self, validated_data):
        return Registration.objects.create_registration(**validated_data)

class RegistrationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email')


class RegistrationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('code',)


class RegistrationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('is_active',)

    def update(self, instance, validated_data):
        try:
            if validated_data['is_active'] != None:
                instance.is_active = validated_data['is_active']
        except:
            pass
        instance.save()
        return instance


class CoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinator
        fields = ('name', 'contact_num')