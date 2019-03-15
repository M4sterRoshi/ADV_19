from rest_framework import status, exceptions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EventRegistrationSerializer, EventListSerializer, EventDetailSerializer, RegistrationUserSerializer, RegistrationUpdateSerializer, CoordinatorSerializer, RegistrationEventSerializer
from .renderers import EventJSONRenderer
from .getters import EventGetter, RegistrationGetter, CoordinatorGetter, TagGetter

class EventRegistration(APIView):
    permission_classes = (IsAuthenticated,)
    registration_serializer_class = EventRegistrationSerializer
    event_getter = EventGetter
    renderer_classes = (EventJSONRenderer,)
    def post(self, request):
            data = request.data.get('event', {})
            data['user'] = request.user.pk
            data['event'] = self.event_getter.get_event_by_code(data['code']).pk
            if len(request.user.registration_set.filter(event=data['event']).filter(is_active=True))>0:
                return Response({'detail':'already registered'}, status=status.HTTP_200_OK)
            if len(request.user.registration_set.filter(event=data['event']).filter(is_active=False))>0:
                reg=request.user.registration_set.filter(event=data['event']).filter(is_active=False)[0]
                reg.is_active = True
                reg.save()
                return Response({'detail':'success'}, status=status.HTTP_200_OK)
            registration_serializer = self.registration_serializer_class(data=data)
            registration_serializer.is_valid(raise_exception=True)
            registration_serializer.save()
            return Response({'detail':'success'}, status=status.HTTP_201_CREATED)

class EventList(APIView):
    permission_classes = (AllowAny,)
    event_serializer_class = EventListSerializer
    event_getter = EventGetter

    def get(self, request):
        event_list = self.event_getter.get_all_events()
        event_serializer = self.event_serializer_class(event_list, many=True)
        return_data = event_serializer.data
        return Response(event_serializer.data, status=status.HTTP_200_OK)


class EventDetail(APIView):
    permission_classes = (AllowAny,)
    event_serializer_class = EventDetailSerializer
    coordinator_serializer_class = CoordinatorSerializer
    event_getter = EventGetter
    coordinator_getter = CoordinatorGetter


    def get(self, request, code):
        data = code
        event = self.event_getter.get_event_by_code(data)
        event_serializer = self.event_serializer_class(event)
        return_data = event_serializer.data
        coordinators = self.coordinator_getter.get_coordinator_by_event(event.pk)
        coordinator_serializer = self.coordinator_serializer_class(coordinators, many=True)
        return_data['coordinator'] = coordinator_serializer.data
        return Response(return_data, status=status.HTTP_200_OK)


class EventRegistrationView(APIView):
    permission_classes = (IsAuthenticated,)
    event_getter = EventGetter
    registration_getter = RegistrationGetter
    user_serializer_class = RegistrationUserSerializer
    def get(self, request):
        if not request.user.is_staff:
            msg = 'Not Authorized'
            raise exceptions.PermissionDenied(msg)
        data = request.data.get('event', {})
        event = self.event_getter.get_event_by_code(data['code'])
        registrations = self.registration_getter.get_registrations_by_event(event.pk)
        return_data = {}
        for registration in registrations:
            user = registration.user
            user_serializer = self.user_serializer_class(user)
            return_data[str(user)] = user_serializer.data
        return Response({'registrations':return_data}, status=status.HTTP_200_OK)


class RegistrationUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    registration_serializer_class = RegistrationUpdateSerializer

    def post(self, request):
        data = request.data.get('registration', {})
        user = request.user
        event = EventGetter.get_event_by_code(data['event'])
        reg = user.registration_set.filter(event=event).first()
        print(reg, data)
        serializer = self.registration_serializer_class(reg, data=data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({'detail':'success'}, status=status.HTTP_200_OK)


class UserRegisteredEventsView(APIView):
    permission_classes = (IsAuthenticated,)
    event_serializer_class = RegistrationEventSerializer
    registration_getter_class = RegistrationGetter
    event_getter_class = EventGetter

    def get(self, request):
        user = request.user
        registrations = self.registration_getter_class.get_registrations_by_user(user.pk)
        events = []
        for r in registrations:
            events.append(self.event_getter_class.get_event_by_registration(r.pk))
        event_serializer = self.event_serializer_class(events, many=True)
        return Response(event_serializer.data, status=status.HTTP_200_OK)
