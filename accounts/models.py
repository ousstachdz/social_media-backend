from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class AppUser(User):

    address = models.TextField()
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='staff_images')

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(AppUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Conversation(models.Model):

    class Meta:
        ordering = ['timestamp']

    timestamp = models.DateTimeField(auto_now_add=True)
    user1 = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name='user2')

    def __str__(self):
        return self.user1.username + ' ' + self.user2.username


class Message(models.Model):

    class Meta:
        ordering = ['timestamp']

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name='receiver')
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.content
