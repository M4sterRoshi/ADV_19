from .models import User
from event.models import Event, Tag
from rest_framework import exceptions

class UserGetter:
    def get_all_users():
        return User.objects.all()

    def get_user_by_pk(pk):
        try:
            return User.objects.get(pk=pk)
        except:
            msg = 'Invalid User key.'
            raise exceptions.NotFound(msg)
    
    def get_user_by_event_registration(registration):
        try:
            return registration.user
        except:
            msg = 'Invalid Registration'
            raise exceptions.NotFound(msg)

