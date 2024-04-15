from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q

from .models import AppUser, Conversation, Message, FriendRequest
from .serializers import AppUserSerializer, ConversationSerializer, ConversationBaseSerializer, AppUserFriendshipSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user(request):
    user = AppUser.objects.all().filter(id=request.user.id).first()
    serialized = AppUserSerializer(user, many=False,)
    return Response(serialized.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user_by_id(request, id):

    user = AppUser.objects.all().filter(id=id).first()
    if user:
        serialized = AppUserSerializer(user, many=False)
        return Response(serialized.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_user(request, kw):
    query = Q(username__contains=kw) | Q(email__contains=kw) | Q(
        first_name__contains=kw) | Q(last_name__contains=kw)
    user = AppUser.objects.all().filter(query)
    if user:
        serialized = AppUserFriendshipSerializer(
            user, many=True, context={'user_id': request.user.id})
        return Response(serialized.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_user(request):
    serialized = AppUserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_conversation(request, id):
    print(id)
    print(request.user.id)

    queryset = Q(user1=id, user2=request.user.id) | Q(
        user1=request.user.id, user2=id)
    conversations = Conversation.objects.all().filter(queryset).first()
    print(conversations)

    if conversations:
        serialized = ConversationSerializer(
            conversations, many=False, context={'user1_id': request.user.id, 'user2_id': id})
        return Response(serialized.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_conversation(request):
    queryset = Q(user2=request.user.id) | Q(
        user1=request.user.id)
    conversations = Conversation.objects.all().filter(queryset)
    if conversations:
        serialized = ConversationBaseSerializer(conversations, many=True)
        return Response(serialized.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def send_friend_request(request):
    sender = AppUser.objects.all().filter(id=request.user.id).first()
    receiver = AppUser.objects.all().filter(
        id=request.data['receiver']).first()

    if receiver:
        query = Q(sender=sender, receiver=receiver) | Q(
            sender=receiver, receiver=sender)

        friendRequest = FriendRequest.objects.all().filter(query).first()

        if friendRequest:
            return Response(status=status.HTTP_200_OK)
        else:
            friendRequest = FriendRequest.objects.create(
                sender=sender, receiver=receiver).save()
        return Response(status=status.HTTP_201_CREATED)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def accept_friend_request(request):
    sender = AppUser.objects.all().filter(id=request.data['sender']).first()
    receiver = AppUser.objects.all().filter(id=request.user.id).first()
    if sender:
        query = Q(sender=sender, receiver=receiver)

        friendRequest = FriendRequest.objects.all().filter(query).first()

        if friendRequest:
            friendRequest.is_accepted = True
            friendRequest.save()
            conversation = Conversation.objects.create(
                user1=sender, user2=receiver)
            conversation.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def deny_friend_request(request):
    sender = AppUser.objects.all().filter(id=request.data['sender']).first()
    receiver = AppUser.objects.all().filter(id=request.user.id).first()

    if sender:
        query = Q(sender=sender, receiver=receiver)

        friendRequest = FriendRequest.objects.all().filter(query).first()

        if friendRequest:
            friendRequest.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def unfriend(request):
    query = Q(sender=request.user.id, receiver=request.data['receiver']) | Q(
        sender=request.data['receiver'], receiver=request.user.id)
    friendRequest = FriendRequest.objects.all().filter(query).first()
    if friendRequest:
        friendRequest.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def unfollowed(request):
    friendRequest = FriendRequest.objects.all().filter(
        sender=request.user.id, receiver=request.data['receiver']).first()
    if friendRequest:
        friendRequest.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
