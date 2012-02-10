"""Models for the request logger app."""
from django.db import models
from django.contrib.auth.models import User
from forty_two_test_stilgar.helpers.model_helpers import ExtendedModel


class Request(ExtendedModel):
    """Request log model."""
    time = models.DateTimeField(auto_now_add=True)
    """Request date and time."""
    path = models.CharField(max_length=8192)
    """Value of HttpRequest.path_info."""
    host = models.CharField(max_length=256)
    """Result of HttpRequest.get_host()."""
    url = models.CharField(max_length=8192)
    """Result of HttpRequest.build_absolute_uri()."""
    method = models.CharField(max_length=128)
    """Value of HttpRequest.method (usually "GET" or "POST")."""
    referer = models.CharField(max_length=8192, null=True)
    """Value of HttpRequest.META[HTTP_REFERER]."""
    user = models.ForeignKey(User, null=True)
    """Value of HttpRequest.user.id ."""
    request = models.TextField()
    """String representation of HttpRequest object."""
