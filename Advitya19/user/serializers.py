from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User

        fields = ['email', 'name', 'password', 'token', 'gender', 'need_accomodation', 'institution', 'contact_number']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'name': user.name,
            'token': user.token
        }


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'institution', 'need_accomodation', 'gender')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'institution', 'need_accomodation', 'gender', 'contact_number')

    def update(self, instance, validated_data):
        try:
            if validated_data['password'] != None:
                instance.set_password(validated_data['password'])
        except:
            pass
        
        try:
            if validated_data['name'] != None:
                instance.name = validated_data['name']
        except:
            pass

        try:
            if validated_data['email'] != None:
                instance.email = validated_data['email']
        except:
            pass

        try:
            if validated_data['institution'] != None:
                instance.institution = validated_data['institution']
        except:
            pass

        try:
            if validated_data['need_accomodation'] != None:
                instance.need_accomodation = validated_data['need_accomodation']
        except:
            pass

        try:
            if validated_data['gender'] != None:
                instance.gender = validated_data['gender']
        except:
            pass
        
        try:
            if validated_data['contact_number'] != None:
                instance.gender = validated_data['contact_number']
        except:
            pass

        instance.save()
        return instance