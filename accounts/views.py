from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q

from .models import AppUser, Conversation, Message
from .serializers import AppUserSerializer, ConversationSerializer, ConversationBaseSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user(request):
    print(request.user)
    user = AppUser.objects.all().filter(id=request.user.id).first()
    serialized = AppUserSerializer(user, many=False)
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
# Create your views here.


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
    queryset = Q(user1=id, user2=request.user.id) | Q(
        user1=request.user.id, user2=id)
    conversations = Conversation.objects.all().filter(queryset).first()
    if conversations:
        serialized = ConversationSerializer(conversations, many=False)
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
