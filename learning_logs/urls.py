"""Defines URL patterns for learning_logs."""

from unicodedata import name
from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # path mapping URLs to views
    # Home page.
    path('', views.index, name='index'),
    # Page that show all topics.
    path('topics/', views.topics, name='topics'),
    # Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
]
