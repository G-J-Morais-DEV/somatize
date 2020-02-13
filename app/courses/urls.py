from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('details/<slug:slug>', details, name='details'),
    path('inscricao/<slug:slug>', enrollment, name='enrollment'),
    path('anuncios/<slug:slug>', announcements, name='announcements'),
    path('cancelar_inscricao/<slug:slug>',
         undo_enrollment, name='undo_enrollment'),
    path('anuncios/<slug:slug>/<int:pk>',
         show_announcement, name='show_announcements'),
    path('aulas/<slug:slug>', lessons, name='lessons'),
    path('aula/<slug:slug>/<int:pk>', lesson, name='lesson'),
]
