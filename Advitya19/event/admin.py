from django.contrib import admin
from .models import Event, Coordinator, Registration, Tag, Organizer

admin.site.register(Event)
admin.site.register(Coordinator)
admin.site.register(Registration)
admin.site.register(Tag)
admin.site.register(Organizer)