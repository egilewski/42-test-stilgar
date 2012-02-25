"""Registering user profile models for admin site."""
from django.contrib import admin
from forty_two_test_stilgar.apps.user_profile.models import Profile

admin.site.register(Profile)
