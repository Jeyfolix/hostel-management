from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Hostel, HostelImage, Booking

# Inline for hostel images
class HostelImageInline(admin.TabularInline):
    model = HostelImage
    extra = 1
    max_num = 5  # Limit to 5 images as requested
    fields = ['image', 'caption', 'is_primary', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "(No image)"
    image_preview.short_description = 'Preview'

# Custom form for hostel
class HostelAdminForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

# Hostel Admin
@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    form = HostelAdminForm
    inlines = [HostelImageInline]
    list_display = [
        'name', 
        'hostel_type', 
        'location_display', 
        'price_display', 
        'rooms_status', 
        'availability_status', 
        'thumbnail_preview'
    ]
    list_filter = ['hostel_type', 'location', 'is_available']
    search_fields = ['name', 'description', 'address', 'warden_name']
    readonly_fields = ['thumbnail_preview', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'hostel_type', 'location', 'address', 'description')
        }),
        ('Pricing & Capacity', {
            'fields': ('price_per_semester', 'total_rooms', 'rooms_available')
        }),
        ('Contact Information', {
            'fields': ('warden_name', 'warden_contact', 'contact_email', 'contact_phone')
        }),
        ('Amenities', {
            'fields': (
                'has_wifi', 'has_kitchen', 'has_laundry', 'has_shower', 
                'has_pool', 'has_gym', 'has_study_room', 'has_parking', 'has_security'
            )
        }),
        ('Status', {
            'fields': ('is_available', 'rating', 'thumbnail_preview')
        }),
        ('Admin Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def location_display(self, obj):
        return obj.get_location_display()
    location_display.short_description = 'Location'
    
    def price_display(self, obj):
        return f"KES {obj.price_per_semester:,.2f}"
    price_display.short_description = 'Price/Sem'
    
    def rooms_status(self, obj):
        booked = obj.total_rooms - obj.rooms_available
        return f"{booked}/{obj.total_rooms} booked"
    rooms_status.short_description = 'Occupancy'
    
    def availability_status(self, obj):
        if obj.is_available and obj.rooms_available > 0:
            color = 'green'
            text = 'Available'
        elif obj.is_available:
            color = 'orange'
            text = 'Fully Booked'
        else:
            color = 'red'
            text = 'Not Available'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    availability_status.short_description = 'Status'
    
    def thumbnail_preview(self, obj):
        # Get primary image or first image
        primary_image = obj.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = obj.images.first()
        
        if primary_image and primary_image.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; border-radius: 5px;" />',
                primary_image.image.url
            )
        return format_html('<span style="color: #999;">No image uploaded</span>')
    thumbnail_preview.short_description = 'Thumbnail'

# HostelImage Admin
@admin.register(HostelImage)
class HostelImageAdmin(admin.ModelAdmin):
    list_display = ['hostel', 'image_preview', 'is_primary', 'uploaded_at']
    list_filter = ['hostel', 'is_primary']
    search_fields = ['hostel__name', 'caption']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

# Booking Admin - FIXED VERSION
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_id', 
        'hostel_name', 
        'student_name', 
        'student_id', 
        'semester', 
        'status',  # Added status to list_display
        'status_badge', 
        'booked_at'
    ]
    list_filter = ['status', 'hostel', 'booked_at']
    search_fields = ['student_name', 'student_email', 'student_id', 'hostel__name']
    readonly_fields = ['booked_at']
    list_editable = ['status']  # Now status is also in list_display
    
    def booking_id(self, obj):
        return f"BK-{obj.id:04d}"
    booking_id.short_description = 'Booking ID'
    
    def hostel_name(self, obj):
        return obj.hostel.name
    hostel_name.short_description = 'Hostel'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'cancelled': 'red',
            'completed': 'blue',
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 12px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status Badge'
