from django.contrib import admin
from .models import AppUser, Conversation, Message, FriendRequest


admin.site.register(AppUser)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(FriendRequest)
# Register your models here.
