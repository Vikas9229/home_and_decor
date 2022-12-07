
from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from .serializer import UserSerializer

from .models import CustomUser 
# Create your views here.

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listEmplyees(request):
    id = request.GET.get('id')
    if id is not None:
        user = CustomUser.objects.filter(id=id)
        user_ser = UserSerializer(user,many=True).data
        return Response(data=user_ser,status=status.HTTP_200_OK)
    user = CustomUser.objects.all()
    user_ser = UserSerializer(user,many=True).data
    return Response(data=user_ser,status=status.HTTP_200_OK)