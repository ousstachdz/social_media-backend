from django.contrib import admin
from .models import AppUser, Conversation, Message

admin.site.register(AppUser)
admin.site.register(Conversation)
admin.site.register(Message)
# Register your models here.
