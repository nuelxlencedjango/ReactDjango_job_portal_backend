
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics, serializers, status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from artisans.models import *
from accounts.serializers import *
from employers.models import *
from employers.serializers import *
from django.db import transaction
import json





class EmployerCreateView(generics.CreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user_data = self.request.data.get('user', {})

        if not isinstance(user_data, dict):
            raise serializers.ValidationError({'user': 'Invalid user data'})

        user_data['is_employer'] = True
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            try:
                with transaction.atomic():
                    user = user_serializer.save()
                    user.set_password(user_data.get('password', ''))
                    user.save()
                    serializer.save(user=user)
            except Exception as e:
                raise serializers.ValidationError({'detail': f"An error occurred while saving user data: {str(e)}"})
        else:
            raise serializers.ValidationError(user_serializer.errors)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return response
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as e:
            return Response({'errors': f"Invalid JSON data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors': f"An unknown error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EmployerSearchListView(generics.ListAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['employer_profile__location__location', 'industry__name']
    search_fields = ['user__first_name', 'user__last_name']





#job search list
class JobSearchListView(generics.ListAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['location', 'job_type', 'industry']
    search_fields = ['title', 'description', 'industry']




class lpOrderRequestView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data.copy()
        data['employer'] = request.user.id

        serializer = OrderRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class lpOrderRequestCreateView(generics.CreateAPIView):
    queryset = OrderRequest.objects.all()
    serializer_class = OrderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        artisan_id = self.request.data.get('artisan_id')
        service_id = self.request.data.get('service_id')

        try:
            artisan = Artisan.objects.get(pk=artisan_id)
            service = Service.objects.get(pk=service_id)
        except (Artisan.DoesNotExist, Service.DoesNotExist):
            raise serializers.ValidationError("Invalid Artisan or Service")

        serializer.save(artisan=artisan, service=service, employer=self.request.user.employer)



class OrderRequestCreateView(generics.CreateAPIView):
    queryset = OrderRequest.objects.all()
    serializer_class = OrderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        artisan_id = self.request.data.get('artisan')
        service_id = self.request.data.get('service')

        try:
            artisan = Artisan.objects.get(pk=artisan_id)
            service = Service.objects.get(pk=service_id)
        except (Artisan.DoesNotExist, Service.DoesNotExist):
            raise serializers.ValidationError("Invalid Artisan or Service")

        serializer.save(artisan=artisan, service=service, employer=self.request.user.employer)
