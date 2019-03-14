from django.urls import path, include

urlpatterns = [
    path('event/', include('event.urls')),
    path('user/', include('user.urls')),
]