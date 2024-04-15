from django.urls import path

from . import views


urlpatterns = [

    path(route='get_user',
         view=views.get_user,
         name='get_user'),

    path(route='get_user_by_id/<str:id>',
         view=views.get_user_by_id,
         name='get_user_by_id'),

    path(route='search_user/<str:kw>',
         view=views.search_user,
         name='search_user'),

    path(route='create_user',
         view=views.create_user,
         name='create_user'),

    path(route='get_conversation/<str:id>',
         view=views.get_conversation,
         name='get_conversation'),

    path(route='get_all_conversation',
         view=views.get_all_conversation,
         name='get_all_conversation'),

    path(route='send_friend_request/',
         view=views.send_friend_request,
         name='send_friend_request'),

    path(route='accept_friend_request/',
         view=views.accept_friend_request,
         name='accept_friend_request'),

    path(route='deny_friend_request/',
         view=views.deny_friend_request,
         name='deny_friend_request'),

    path(route='unfriend/',
         view=views.unfriend,
         name='unfriend'),
    path(route='unfollowed/',
         view=views.unfollowed,
         name='unfollowed'),



]
