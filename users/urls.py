"""Defines URL patterns for users"""

from django.urls import path, include

# We set the variable app_name to 'users' so Django can distinguish
# these URLs from URLs belonging to other apps.
app_name = 'users'
urlpatterns = [
    # Inlcude default auth urls.
    path('', include('django.contrib.auth.urls')),
]
