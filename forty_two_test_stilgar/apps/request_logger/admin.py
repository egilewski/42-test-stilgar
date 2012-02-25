"""Registering request logger models for admin site."""
from django.contrib import admin
from forty_two_test_stilgar.apps.request_logger.models import Request

admin.site.register(Request)
