"""
URL configuration for Event_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('event', views.handle_event),
    path('event/<str:id>', views.handle_specified_event),
    path('event/<str:event_id>/rsvp', views.create_rsvp),
    path('event/<str:event_id>/rsvp/<str:user_id>', views.update_rsvp),
    path('event/<str:id>/reviews', views.handle_reviews),
    # path('delete/<str:id>', views.delete_event),
]
