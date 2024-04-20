from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsServiceProvider
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Service, ServiceProvider, Booking, Review
from .serializers import ServiceSerializer, ServiceProviderSerializer, BookingSerializer, ReviewSerializer, BookingSerializer
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegisterForm

# ViewSets
class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user and request.user.is_authenticated  # Allow any authenticated user to view
        return request.user.is_authenticated and getattr(request.user, 'is_service_provider', False)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().select_related('provider')
    serializer_class = ServiceSerializer
    permission_classes = [CustomPermission]

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.user.is_superuser:
        # Allow all actions for superusers
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only service providers can perform these actions
            permission_classes = [IsServiceProvider]
        else:
            # Any user can list or retrieve service providers
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all().select_related('client', 'service')
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         # Set the client to the logged-in user
#         serializer.save(client=self.request.user.client)

#     @action(detail=True, methods=['post'])
#     def confirm_booking(self, request, pk=None):
#         """
#         Custom action to confirm a booking.
#         """
#         booking = self.get_object()
#         if booking.client.user != request.user:
#             return Response({'error': 'You do not have permission to confirm this booking'}, status=status.HTTP_403_FORBIDDEN)
#         booking.status = 'confirmed'
#         booking.save()
#         return Response({'status': 'booking confirmed'})
        
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related('service', 'service__provider')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Optionally, set the client automatically from the request user, if the client field isn't expected in the request
        serializer.save(client=self.request.user.client)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('booking')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all().select_related('service', 'service__provider')
#     serializer_class = BookingSerializer

#     # Require user to be authenticated to create a booking
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['post'], name='Create Booking')
#     def create_booking(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # Save the new booking
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related('service', 'service__provider')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Optionally, set the client automatically from the request user, if the client field isn't expected in the request
        serializer.save(client=self.request.user.client)


# Generic views for user registration and static pages
class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
