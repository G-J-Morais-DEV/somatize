from django.contrib import admin
from django.urls import path
from .views import ForumView, ThreadView, ReplyCorrectView

urlpatterns = [
    path('', ForumView.as_view(), name='forum'),
    path('tag/<str:tag>', ForumView.as_view(), name='forum_tagged'),
    path('tópico/<slug:slug>', ThreadView.as_view(), name='thread'),
    path('resposta_correta/<int:pk>',
         ReplyCorrectView.as_view(), name='reply_correct'),
    path('resposta_incorreta/<int:pk>',
         ReplyCorrectView.as_view(correct=False), name='reply_incorrect'),
]
