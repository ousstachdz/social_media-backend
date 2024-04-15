from rest_framework import serializers
from django.utils import timezone
from django.db.models import Q
from .models import AppUser, Message, Conversation, FriendRequest


class AppUserBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = (
            'id', 'first_name', 'last_name', 'username',
            'photo'
        )


class AppUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)

    def validate_date_of_birth(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Date of birth can't be in the future")
        if value.year < 1900:
            raise serializers.ValidationError(
                "Date of birth can't be before 1900")
        min_date = timezone.now().date().year - 18
        if value.year > min_date:
            raise serializers.ValidationError(
                "You must be 18 years old to register")
        return value

    class Meta:
        model = AppUser
        fields = (
            'id', 'first_name', 'last_name', 'username',
            'photo', 'address', 'date_of_birth',
            'password'
        )


class AppUserFriendshipSerializer(serializers.ModelSerializer):

    is_follower = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)

    def get_is_follower(self, obj):

        user_id = self.context.get('user_id', None)

        if FriendRequest.objects.filter(sender=obj, receiver=user_id).exists():
            return True
        else:
            return False

    def get_is_followed(self, obj):

        user_id = self.context.get('user_id', None)

        if FriendRequest.objects.filter(receiver=obj, sender=user_id).exists():
            return True
        else:
            return False

    def get_is_friend(self, obj):

        user_id = self.context.get('user_id', None)
        query = Q(sender=obj, receiver=user_id) | Q(
            sender=user_id, receiver=obj)

        friendRequest = FriendRequest.objects.all().filter(query).first()
        if friendRequest:
            if friendRequest.is_accepted:
                return True
            else:
                return False
        else:
            return False

    class Meta:
        model = AppUser
        fields = (
            'id', 'first_name', 'last_name', 'username',
            'photo', 'address', 'date_of_birth',
            'password',
            "is_follower", "is_followed",
            'is_friend'
        )


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id', 'content', 'timestamp', 'sender', 'receiver',
        )


class ConversationBaseSerializer(serializers.ModelSerializer):

    user1 = AppUserBaseSerializer()
    user2 = AppUserBaseSerializer()

    last_message = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Conversation
        fields = (
            'id', 'timestamp', 'user1', 'user2', 'last_message'
        )

    def get_last_message(self, obj):
        messages = Message.objects.filter(
            conversation=obj).order_by('-timestamp').first()
        serialized_messages = MessageSerializer(messages, many=False)
        return serialized_messages.data


class ConversationSerializer(serializers.ModelSerializer):

    # user1 = AppUserBaseSerializer()
    # user2 = AppUserBaseSerializer()
    user1 = serializers.SerializerMethodField()
    user2 = serializers.SerializerMethodField()

    messages = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Conversation
        fields = (
            'id', 'timestamp', 'user1', 'user2', 'messages'
        )

    def get_messages(self, obj):
        messages = Message.objects.filter(conversation=obj)
        serialized_messages = MessageSerializer(messages, many=True)
        return serialized_messages.data

    def get_user1(self, obj):
        user_id = self.context.get('user1_id', None)
        user = AppUser.objects.all().filter(id=user_id).first()
        serialized_user = AppUserBaseSerializer(user, many=False)
        return serialized_user.data

    def get_user2(self, obj):
        user_id = self.context.get('user2_id', None)
        user = AppUser.objects.all().filter(id=user_id).first()
        serialized_user = AppUserBaseSerializer(user, many=False)
        return serialized_user.data
