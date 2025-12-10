from django.contrib import admin
from .models import UserProfile, Event, RSVP, Review


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "location")
    search_fields = ("full_name", "user__username")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "organizer", "start_time", "end_time", "is_public")
    search_fields = ("title", "organizer__username")
    list_filter = ("is_public", "start_time")
    filter_horizontal = ("invited",)   # For selecting invited users in admin


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("event__title", "user__username")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("event__title", "user__username")
