from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from pokedex.views import (
    SetViewSet,
    CardViewSet,
)


urlpatterns = [
    # path('', include('rest_framework.urls')),

    path('sets/', SetViewSet.as_view({
        'get': 'list', 'post': 'create',
    }), name='set-list'),
    path('sets/<str:slug>/', SetViewSet.as_view({
        'get': 'retrieve', 'delete': 'destroy'
    }), name='set-detail'),

    path('sets/<str:slug>/cards/', CardViewSet.as_view({
        'get': 'list', 'post': 'create',
    }), name='card-list'),
    path('sets/<str:set_slug>/cards/<str:slug>/', CardViewSet.as_view({
        'get': 'retrieve', 'delete': 'destroy'
    }), name='card-detail'),

    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)