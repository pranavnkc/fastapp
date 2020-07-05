#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Python imports.
# Django imports.
from django.conf.urls import url

# Rest Framework imports.
from rest_framework.routers import DefaultRouter
# Third Party Library imports

# local imports.
from service.views import (
    TestAppAPIView, 
    UserAPIView, 
    ServiceViewSet,
    RegistrationAPIView,
    LoginView,
    LogoutView
)

app_name = 'service_app'
router = DefaultRouter()
router.register(r'service', ServiceViewSet, base_name="service")
urlpatterns = router.urls
urlpatterns += [
    url(r'^test/$', TestAppAPIView.as_view(), name='service_app'),
    url(r'^register/$', RegistrationAPIView.as_view(), name='register-api'),
    url(r'^login/$', LoginView.as_view(), name='login-api'),
    url(r'^logout/$', LogoutView.as_view(), name='logout-api'),
    url(r'^list/users/$', UserAPIView.as_view(), name='user-api'),
]
