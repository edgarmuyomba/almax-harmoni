from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Service, ServiceProvider, Booking, Review
from django.utils import timezone

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        exclude = ('user',)

class ServiceSerializer(serializers.ModelSerializer):
    provider_details = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_provider_details(self, obj):
        """
        Method to return the details of the provider of the service.
        """
        serializer = ServiceProviderSerializer(obj.provider)
        return serializer.data
    
    def validate_price(self, value):
        """
        Check that the price is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("The price must be a positive number.")
        return value

class BookingSerializer(serializers.ModelSerializer):
    service_details = serializers.SerializerMethodField()
    provider_details = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status']

    def get_service_details(self, obj):
        if obj.service:
            serializer = ServiceSerializer(obj.service)
            return serializer.data
        return None

    def get_provider_details(self, obj):
        if obj.service and obj.service.provider:
            serializer = ServiceProviderSerializer(obj.service.provider)
            return serializer.data
        return None

    def validate(self, data):
        if 'booking_date' in data and data['booking_date'] < timezone.now():
            raise ValidationError("Booking cannot be made for a past date.")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if not hasattr(request.user, 'client'):
            raise ValidationError("This user does not have a client profile.")
        validated_data['client'] = request.user.client
        return super().create(validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['booking', 'reviewer'],
                message="One review per booking per reviewer."
            )
        ]
