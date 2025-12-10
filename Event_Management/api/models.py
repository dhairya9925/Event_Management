from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    # invites = models.ManyToManyField()

    def __str__(self):
        return self.full_name or self.user.username


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)
    invited = models.ManyToManyField(User, related_name="invited_people", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# RSVP -> "Please Respons"
class RSVP(models.Model):
    STATUS_CHOICES = [
        ('going', 'Going'),
        ('maybe', 'Maybe'),
        ('Not Going', 'Not Going'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rsvps")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    # This is to ensure that a user only responds to a RSVP once
    class Meta:
        constraints = (models.UniqueConstraint(fields=["event", "user"], name="unique_RSVP"),)  # A user can RSVP only once per event

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"


class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()  # e.g., 1–5 stars
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # This is to ensure that a user can only post one reviewx
    class Meta:
        constraints = (models.UniqueConstraint(fields=["event", "user"], name="unique_review"),)  # One review per event per user
        ordering = ["-created_at"]          # Latest reviews first

    def __str__(self):
        return f"{self.event.title} - {self.rating} by {self.user.username}"