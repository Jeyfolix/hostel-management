from rest_framework import viewsets, filters, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Hostel, Booking
from .serializers import HostelSerializer, BookingSerializer

class HostelViewSet(viewsets.ModelViewSet):
    queryset = Hostel.objects.filter(is_available=True).prefetch_related('images')
    serializer_class = HostelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Removed DjangoFilterBackend
    search_fields = ['name', 'description', 'address', 'location']
    ordering_fields = ['price_per_semester', 'rating', 'created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'locations']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured hostels"""
        featured_hostels = self.get_queryset().order_by('-rating')[:6]
        serializer = self.get_serializer(featured_hostels, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def locations(self, request):
        """Get all available locations with count"""
        locations = []
        for loc_code, loc_name in Hostel.LOCATIONS:
            count = Hostel.objects.filter(location=loc_code, is_available=True).count()
            locations.append({
                'code': loc_code,
                'name': loc_name,
                'count': count
            })
        return Response(locations)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Booking.objects.all()
            # For regular users, return their bookings by email
            return Booking.objects.filter(student_email=self.request.user.email)
        return Booking.objects.none()
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]  # Anyone can create a booking
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
