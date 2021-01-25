from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
    path('', views.list),
    path('create/', views.create),
    path('edit/', views.edit),
    path('delete/', views.delete),
    path('view/', views.view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
