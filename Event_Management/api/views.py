from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Event, Review, RSVP, UserProfile
from .serializer import EventSerializer, ReviewSerializer, RSVPSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user 

# Create your views here.
@api_view(["GET"])
def home(request):
    return Response({"status": f"Healthy"})


def handle_event(request):
    try:
        if request.method == "GET":
            return all_event(request)
        elif request.method == "POST":
            return create_event(request)
    except Exception as e:
        return Response({"Error": f"{e}"})
    return Response({"messsage": f"Something Went Worng!!"})

def handle_specified_event(request, id):
    try:
        if request.method == "GET":
            return view_event(request, id)
        elif request.method == "PUT":
            return update_event(request, id)
        elif request.method == "DELETE":
            return delete_event(request, id)
    except Exception as e:
        return Response({"Error": f"{e}"})
    return Response({"messsage": f"Something Went Worng!!"})
    


# @api_view(["POST"])
def create_event(request):
    # if request.method == "POST":
    try:
        event = Event(
            title = request.data.get('title'),
            description = request.data.get('description'),
            organizer = request.data.get('organizer'),
            location = request.data.get('location'),
            start_time = request.data.get('start_time'),
            end_time = request.data.get('end_time'),
            is_public = request.data.get('is_public'),
        )
        event.save()
    except Exception as e:
        return Response({"Error": f"{e}"})
    return Response({"messsage": f"Something Went Worng!!"})


# @api_view(["GET"])
def all_event(request):
    try:
        events_all = Event.objects.all()
        serializer = EventSerializer(events_all, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": f"{e}"})


@api_view(["GET"])
def view_event(request, id):
    try:
        event = Event.objects.get(id=id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": f"{e}"})


@api_view(["PUT"])
def update_event(request, id):
    try:
        event = Event.objects.get(id = id)
        
        event.title = request.data.get('title'),
        event.description = request.data.get('description'),
        event.organizer = request.data.get('organizer'),
        event.location = request.data.get('location'),
        event.start_time = request.data.get('start_time'),
        event.end_time = request.data.get('end_time'),
        event.is_public = request.data.get('is_public'),

        event.save()
        serializer = EventSerializer(event)

        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": f"{e}\n\nFailed to update"})


@api_view(["DELETE"])
def delete_event(request, id):
    try:    
        event = Event.objects.get(id = id)
        serializer = EventSerializer(event)
        event.delete()
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": f"{e}\n\nFailed to delete"})


@api_view(["POST"])
def create_rsvp(request, event_id   ):
    try:
        event = Event.objects.get(id=event_id)
        user = UserProfile.objects.get(user=get_user(request))
        
        rsvp, created = RSVP.objects.get_or_create(
            event = event,
            user = user,
        )

        if created:
            rsvp.status = request.data.get("status")
            rsvp.save()
        else:
            return Response({"message": f"RSVP Already Exist for {user.username} on {event.title}"})

        serializer = RSVPSerializer(rsvp)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": f"{e}"})


@api_view(["PATCH"])
def update_rsvp(request, event_id, user_id):
    try:
        event = Event.objects.get(id=event_id)
        user = UserProfile.objects.get(id=user_id)
        rsvp = RSVP.objects.get(id=id)

        rsvp.event = request.data.get("event")
        rsvp.user = request.data.get("user")
        rsvp.status = request.data.get("status")

    except Exception as e:
        return Response({"Error": f"{e}"})
    return Response({"messsage": f"Something Went Worng!!"})
        

def handle_reviews(request, event_id):
    try:
        if request.method == "POST":
            add_review(request, event_id)
        elif request.method == "GET":
            list_reviews(request, event_id)
        else:
            raise Exception
    except Exception as e:
        return Response({"Error": f"{e}"})
    return Response({"messsage": f"Something Went Worng!!"})


def add_review(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        user = UserProfile.objects.get(user=get_user(request))
        review, created = Review.objects.get_or_create(
            event = event,
            user = user
        )
        if created:                
            if request.data.get("frating") > 5 or request.data.get("rating") <= 0 :
                return Response({"error": "Invalid Value for rating"})
            review.rating = request.data.get("rating")
            review.comment = request.data.get("comment")
            review.save()

            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response({"error": f"{user.full_name} already reviewed {event.title}"})
    except Exception as e:
        return Response({"error": f"{e}"})


def list_reviews(request, event_id):
    try:
        event = Event.objects.get(id = event_id)
        reviews = Review.objects.filter(event=event)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": f"{e}"})

