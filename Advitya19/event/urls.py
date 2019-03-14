from django.urls import path, include
from .views import EventRegistration, EventList, EventDetail, EventRegistrationView, RegistrationUpdate

urlpatterns = [
    path('register', EventRegistration.as_view()),
    path('list', EventList.as_view()),
    path('detail/<slug:code>', EventDetail.as_view()),
    path('registrations', EventRegistrationView.as_view()),
    path('update', RegistrationUpdate.as_view()),
]