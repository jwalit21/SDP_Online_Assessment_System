"""onlineassessmentsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'users.views.pageNotFound'
handler500 = 'users.views.internalServerError'

urlpatterns = [
    path('', user_views.index),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('classroom/', include('classroom.urls')),
    path('labs/', include('lab.urls')),
    path('contests/', include('contest.urls')),
    path('problems/', include('problem.urls')),
    path('submissions/', include('submissions.urls')),
    path('blogs/', include('blog.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
