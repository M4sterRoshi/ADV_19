from django.urls import path
from .views import UserRegistration, UserLogin, UserView, UserUpdate
from event.views import UserRegisteredEventsView

urlpatterns = [
    path('reg', UserRegistration.as_view()),
    path('login', UserLogin.as_view()),
    path('info', UserView.as_view()),
    path('update', UserUpdate.as_view()),
    path('events', UserRegisteredEventsView.as_view()),
]