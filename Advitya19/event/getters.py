from .models import Event, Coordinator, Registration
from user.getters import UserGetter
from rest_framework import exceptions

class EventGetter:
    def get_all_events():
        return Event.objects.all()

    def get_event_by_pk(pk):
        try:
            return Event.objects.get(pk=pk)
        except:
            msg = 'Invalid event key.'
            raise exceptions.NotFound(msg)
    
    def get_event_by_code(code):
        try:
            return Event.objects.get(code=code)
        except:
            msg = 'Invalid event code.'
            raise exceptions.NotFound(msg)

    def get_event_by_registration(pk):
        registration = RegistrationGetter.get_registration_by_pk(pk)
        try:
            return registration.event
        except:
            msg = 'Bad Registration.'
            raise exceptions.NotFound(msg)


class RegistrationGetter:
    def get_registration_by_pk(pk):
        try:
            return Registration.objects.get(pk=pk)
        except:
            msg = 'Invalid registration key.'
            raise exceptions.NotFound(msg)

    def get_registrations_by_event(pk):
        event = EventGetter.get_event_by_pk(pk)
        try:
            return event.registration_set.filter(is_active=True)
        except:
            msg = 'No registrations'
            raise exceptions.NotFound(msg)

    def get_registrations_by_user(pk):
        user = UserGetter.get_user_by_pk(pk)
        try:
            return user.registration_set.filter(is_active=True)
        except:
            msg = 'No registrations'
            raise exceptions.NotFound(msg)


class CoordinatorGetter:
    def get_coordinator_by_event(pk):
        event = EventGetter.get_event_by_pk(pk)
        try:
            return event.coordinator_set.all()
        except:
            msg = 'No coordinators'
            raise exceptions.NotFound(msg)

class TagGetter:
    def get_tag_by_pk(pk):
        try:
            return Tag.objects.get(pk=pk)
        except:
            msg = 'Invalid Tag key.'
            raise exceptions.NotFound(msg)