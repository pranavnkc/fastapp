# python imports
import requests

# Django imports
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError  

# Rest Framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework.decorators import detail_route
# local imports
from fastapp.permissions import IsClient, IsServiceProvider
from service.models import User, Service
from service.serializers import (UserSerializer, 
                                 ServiceSerializer,
)
from service.utils import generate_jwt_token
from service.tasks import send_service_contact_mail

# Create your views here.


class TestAppAPIView(APIView):

    def get(self, request, format=None):
        try:
            result = add.delay(11, 15)
            print(result)
            return Response({'status': True,
                             'Response': "Successfully Tested"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(APIView):
    __doc__ = "Registration API for user"

    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        data = generate_jwt_token(user, user_serializer.data)
        return Response(data, status=status.HTTP_200_OK)

class LoginView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer
    
    __doc__ = "Log In API for user which returns token"

    @staticmethod
    def post(request):
        serializer = JSONWebTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.validate(request.data)
        user_data = UserSerializer(User.objects.get(username=request.data['username'])).data
        if not user_data['groups']:
            return Response({'groups': "User not registered with any groups."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': True,
            'token': serialized_data['token'],
            'user': user_data,
        }, status=status.HTTP_200_OK)
         
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Logout API for user
        """
        try:
            user = request.data.get('user', None)
            logout(request)
            return Response({'status': True,
                             'message': "logout successfully"},
                            status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False},
                            status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(GenericAPIView):
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        List all the users.
        """
        try:
            users = User.objects.all()
            user_serializer = UserSerializer(users, many=True)

            users = user_serializer.data
            return Response({'status': True,
                             'Response': users},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated,)
    
    def initial(self, *args, **kwargs):        
        if args[0].method in ['POST', "DELETE", ]:
            self.permission_classes = (IsServiceProvider, )
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(ServiceViewSet, self).initial(*args, **kwargs)
    
    def get_queryset(self):
        qs = Service.objects.all()
        if self.request.user.groups.filter(name='service-provider').exists():
            return qs.filter(user=self.request.user)
        return qs
    
    @detail_route(methods=['patch',])
    def contact(self, request, pk):
        print(send_service_contact_mail)
        send_service_contact_mail.delay(request.user.id, pk)
        return Response()
