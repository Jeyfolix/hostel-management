from rest_framework import serializers
from .models import Hostel, HostelImage, Booking

class HostelImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = HostelImage
        fields = ['id', 'image', 'image_url', 'caption', 'is_primary']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class HostelSerializer(serializers.ModelSerializer):
    images = HostelImageSerializer(many=True, read_only=True)
    booked_rooms_count = serializers.SerializerMethodField()
    occupancy_rate = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Hostel
        fields = [
            'id', 'name', 'hostel_type', 'location', 'address', 'description',
            'price_per_semester', 'total_rooms', 'rooms_available',
            'warden_name', 'warden_contact', 'contact_email', 'contact_phone',
            'has_wifi', 'has_kitchen', 'has_laundry', 'has_shower', 'has_pool',
            'has_gym', 'has_study_room', 'has_parking', 'has_security',
            'is_available', 'rating', 'booked_rooms_count', 'occupancy_rate',
            'thumbnail_url', 'images', 'created_at', 'updated_at'
        ]
    
    def get_booked_rooms_count(self, obj):
        return obj.booked_rooms()
    
    def get_occupancy_rate(self, obj):
        return obj.occupancy_rate()
    
    def get_thumbnail_url(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = obj.images.first()
        
        if primary_image and primary_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None

class BookingSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    hostel_location = serializers.CharField(source='hostel.location', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'hostel', 'hostel_name', 'hostel_location',
            'student_name', 'student_email', 'student_phone', 'student_id',
            'semester', 'room_preference', 'special_requests',
            'status', 'booked_at', 'check_in_date', 'check_out_date'
        ]
