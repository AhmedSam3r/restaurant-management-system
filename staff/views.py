from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import  IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken


from .serializers import StaffSerializer, MyTokenObtainPairSerializer, MyTokenObtainPairView
from staff.models import Staff  

import json
from datetime import datetime


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    body = request.data
    try:
        id = request.data.get('id', None)
        password = request.data.get('password', None)
        staff = get_object_or_404(Staff, pk=id, password=password)
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1] if 'HTTP_AUTHORIZATION' in request.META else ''
        decoded_token = AccessToken(token)
        decoded_token.verify()
        if decoded_token:
            #TODO figure out how to send the current refresh token
            return Response({'access':str(token), 'refresh':str(RefreshToken.for_user(staff)),'Message':'User token is still valid', 'success':True}, status=200)
    except (Staff.DoesNotExist, TokenError) as ex:
        print(ex)


    serializer = MyTokenObtainPairSerializer(data=request.data)
    
    if serializer.is_valid():
        refresh_token = serializer.validated_data['refresh']
        access_token = serializer.validated_data['access']
        staff_serialized = serializer.user
        if staff_serialized is not None:
            refresh = RefreshToken.for_user(staff)
            token = {'refresh': str(refresh_token), 'access': str(access_token)}
            return Response(token, status=200)
        
    return Response(serializer.errors, status=400)



@api_view(['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
def create_user(request):
    body = request.data
    name = body['name']
    role = body['role']
    email = body['email']
    password = body['password']
    
    serializer = StaffSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'user_id': user.pk, 'message': 'User created successfully.'}, status=201)
    else:
        return Response(serializer.errors, status=400)

