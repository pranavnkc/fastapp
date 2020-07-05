#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Python imports.
import logging
import datetime
import calendar

# Django imports.
from django.db import transaction

# Rest Framework imports.
from rest_framework import serializers

# Third Party Library imports

# local imports.
from service.models import User, Service


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.SerializerMethodField()
    def get_groups(self, obj):
        return obj.groups.values_list('name', flat=True)
    
    @transaction.atomic()
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name', 'groups')
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True}
        }
        
class ServiceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Service.objects.create(**validated_data)
