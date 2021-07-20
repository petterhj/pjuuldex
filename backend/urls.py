from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, path
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    # PasswordChangeView,
    # PasswordResetConfirmView,
    # PasswordResetView, 
)

from pokedex.views import (
    SetViewSet,
    CardViewSet,
    InventoryViewSet,
)


urlpatterns = [
    path('sets/', SetViewSet.as_view({
        'get': 'list'
    }), name='set-list'),
    path('sets/<str:slug>/', SetViewSet.as_view({
        'get': 'retrieve',
    }), name='set-detail'),
    path('sets/<str:set_slug>/<str:slug>/', CardViewSet.as_view({
        'get': 'retrieve',
    }), name='card-detail'),

    path('user/inventory/variant/<int:variant_pk>/', InventoryViewSet.as_view({
        'get': 'retrieve', 'post': 'create', 'delete': 'destroy'
    }), name='user-card-variant'),
    path('user/inventory/recent/', InventoryViewSet.as_view({
        'get': 'list',
    }), name='user-inventory-recent-list'),

    path("user/", UserDetailsView.as_view(), name="rest_user"),
    path("user/login/", LoginView.as_view(), name="rest_login"),
    # path("user/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("user/logout/", LogoutView.as_view(), name="rest_logout"),

    re_path("^admin/", admin.site.urls),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
