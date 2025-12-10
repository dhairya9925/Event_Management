from rest_framework import serializers
from .models import Event, Review, RSVP, UserProfile 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        # exclude = ("invited",)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

