from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Hostel(models.Model):
    HOSTEL_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Sharing'),
        ('quad', 'Quad Sharing'),
        ('special', 'Special Room'),
        ('apartment', 'Apartment Style'),
    ]
    
    LOCATIONS = [
        ('main_campus', 'Main Campus'),
        ('hill_side', 'Hill Side'),
        ('valley_road', 'Valley Road'),
        ('town_campus', 'Town Campus'),
        ('off_campus', 'Off Campus (Nearby)'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    hostel_type = models.CharField(max_length=20, choices=HOSTEL_TYPES)
    location = models.CharField(max_length=50, choices=LOCATIONS)
    address = models.TextField()
    description = models.TextField(blank=True)
    
    # Pricing & Capacity
    price_per_semester = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.PositiveIntegerField()
    rooms_available = models.PositiveIntegerField()
    
    # Contact Information
    warden_name = models.CharField(max_length=100, blank=True)
    warden_contact = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Amenities (Boolean fields)
    has_wifi = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    has_laundry = models.BooleanField(default=False)
    has_shower = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_study_room = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_security = models.BooleanField(default=False)
    
    # Status
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def booked_rooms(self):
        return self.total_rooms - self.rooms_available
    
    def occupancy_rate(self):
        if self.total_rooms > 0:
            return (self.booked_rooms() / self.total_rooms) * 100
        return 0
    
    class Meta:
        ordering = ['-created_at']


class HostelImage(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hostel_images/')
    caption = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.hostel.name}"
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='bookings')
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()
    student_phone = models.CharField(max_length=20)
    student_id = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    room_preference = models.CharField(max_length=50, blank=True)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.student_name}"
    
    class Meta:
        ordering = ['-booked_at']
