from django.shortcuts import render
from myapp.models import Movies
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .serializers import LoginSerializer,ModelSerializer
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        django_login(request, user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({"token": token.key},status=200)


class LogoutView(APIView):
    authentication_classes=(TokenAuthentication,)
    def post(self,request):
        django_logout(request)
        return Response(status=204)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def movies_list(request):
    if request.method == 'GET':
        movies= Movies.objects.all() 
        title = request.GET.get('title', None)
        reviews=request.GET.get('reviews',None)
        if title is not None:
            movies = movies.filter(title__icontains=title,reviews=reviews)
        
        movies_serializer = ModelSerializer(movies, many=True)
        return JsonResponse(movies_serializer.data, safe=False)

    if request.method == 'POST':
        movies_data = JSONParser().parse(request)
        movies_serializer = ModelSerializer(data=movies_data)
        if movies_serializer.is_valid():
            movies_serializer.save()
            return JsonResponse(movies_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(movies_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
