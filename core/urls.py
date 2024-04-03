from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.settings import VERSION

api_urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{VERSION}/', include('accounts.url'))
]

auth_urlpatterns = [
    path(f'api/{VERSION}/login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path(f'api/{VERSION}/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns = api_urlpatterns + auth_urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
