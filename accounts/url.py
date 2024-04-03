from django.urls import path

from . import views


urlpatterns = [
    path('get_user', views.get_user, name='get_user'),
    path('get_user_by_id/<str:id>', views.get_user_by_id, name='get_user_by_id'),
    path('create_user', views.create_user, name='create_user'),
    path('get_conversation/<str:id>',
         views.get_conversation, name='get_conversation'),
    path('get_all_conversation', views.get_all_conversation,
         name='get_all_conversation'),



]
