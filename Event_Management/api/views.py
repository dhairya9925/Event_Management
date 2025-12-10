from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Event, Review, RSVP, UserProfile
from .serializer import EventSerializer, ReviewSerializer, RSVPSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user
from datetime import datetime
from django.contrib.auth.models import User


# Create your views here.
@api_view(["GET"])
def home(request):
    return Response({"fittness": f"Healthy"})

# _______________________ CREATE AND VIEWS EVENTS _______________________
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def handle_event(request):
    try:
        # _________________View Event_________________
        if request.method == "GET":
            try:        
                print(f"is_authenticated: {request.user.is_authenticated}")
                events_all = Event.objects.all()

                public_events = events_all.filter(is_public = True) 
                invite_events = events_all.filter(invited = request.user) 
                # invite_events = [event for event in events_all if request.user in event.invited.all()]
                user_events = public_events.union(invite_events)

                serializer = EventSerializer(user_events, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"Error": f"{e}"})
        # _________________Create Event_________________
        elif request.method == "POST":
            try:
                print("IN POST")
                # print(f"Ans: {request.data.get('organizer')}, type: {type(int(request.data.get('organizer')))}")
                # id = int(request.data.get('organizer'))
                # print(f"Ans: {request.data.get('organizer')}, id:{id} ,type {type(id)}")

                # Uncomment if you want to make someone else as organizer
                # try:
                #     if request.data.get('organizer') == '':
                #         organizser = request.user
                #     else:
                #         organizser = User.objects.get(username = request.data.get('organizer'))
                # except User.DoesNotExist as e:
                #     Response({"error":e})

                organizser = request.user
                # print(organizser.user.username)
                event = Event(
                    title = request.data.get('title'),
                    description = request.data.get('description'),
                    organizer = organizser,
                    location = request.data.get('location'),
                    start_time = datetime.strptime(request.data.get('start_time'), "%d/%m/%Y %H:%M"),
                    end_time = datetime.strptime(request.data.get('end_time'), "%d/%m/%Y %H:%M"),
                    # end_time = request.data.get('end_time'),
                    is_public = True if request.data.get('is_public') == "y" or request.data.get('is_public').lower() == "yes" else False,
                )

                # invite organizser so they can see the event
                if not event.is_public:
                    event.invited.add(organizser)
                
                event.save()
                serializer = EventSerializer(event)
                return Response(serializer.data)
            except Exception as e:
                raise e
    except Exception as e:
        return Response({"Error": f"{e}"})
    return Response({"messsage": f"Something Went Worng!!"})    

# _______________________ XXXXXXXXXXXXXXXXXXXXXXX _______________________


# ______________________ OPERATE ON SPECIFIC EVENT ______________________
@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def handle_specified_event(request, event_id):
    try:
        # -----------view/get specific event-----------
        if request.method == "GET":
            try:
                event = Event.objects.get(id=event_id)
                serializer = EventSerializer(event)
                return Response(serializer.data)
            except Exception as e:
                return Response({"Error": f"{e}"})

        # -----------Update a specific event-----------
        elif request.method == "PUT":
            try:
                event = Event.objects.get(id = event_id)

                # Check Whether the User trying to update event is Organizer or not 
                if request.user != event.organizer:
                    return Response({"Unauthorized":"Only a organizer can update the event. And Unfortunatly you are not."})

                
                event.title = request.data.get("title")
                event.description = request.data.get("description")
                event.location = request.data.get("location")
                event.start_time = datetime.strptime(request.data.get("start_time"), "%d/%m/%Y %H:%M")
                event.end_time = datetime.strptime(request.data.get("end_time"), "%d/%m/%Y %H:%M")
                event.is_public = request.data.get("is_public")

                event.save()
                serializer = EventSerializer(event)

                return Response(serializer.data)
            except Exception as e:
                return Response({"Error": f"{e}. Failed to update"})

        # -----------Delete a specific event-----------
        elif request.method == "DELETE":
            try:    
                event = Event.objects.get(id = event_id)
                serializer = EventSerializer(event)
                event.delete()
                return Response(serializer.data)
            except Exception as e:
                return Response({"Error": f"{e}Failed to delete"})

    except Exception as e:
        return Response({"Error": f"{e}"})
    return Response({"messsage": f"Something Went Worng!!"})


# ______________________ XXXXXXXXXXXXXXXXXXXXXXXXX ______________________



# _______________________ CREATE AND UPDATE RSVPS _______________________

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_rsvp(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        user = request.user
        
        # Check wether RSVP object with for the user in an event existes, if not create one
        rsvp, created = RSVP.objects.get_or_create(
            event = event,
            user = user,
            defaults={
                "status": request.data.get("status")
            }
        )

        if created:
            rsvp.save()
            serializer = RSVPSerializer(rsvp)
            return Response(serializer.data)
        else:
            return Response({"message": f"RSVP Already Exist for {user.username} on {event.title}"})

    except Exception as e:
        return Response({"Error": f"{e}"})


@api_view(["PATCH"])
def update_rsvp(request, event_id, user_id):
    try:
        event = Event.objects.get(id=event_id)
        user = request.user
        rsvp = RSVP.objects.get(event=event, user=user)

        # rsvp.event = request.data.get("event")
        # rsvp.user = request.data.get("user")
        rsvp.status = request.data.get("status")
        rsvp.save()

        serializer = RSVPSerializer(rsvp)
        return Response(serializer.data)

    except Exception as e:
        return Response({"Error": f"{e}"})
# _______________________ XXXXXXXXXXXXXXXXXXXXXXX _______________________
        

# _________________________ HANDLE EVENT REVIEW _________________________

@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def handle_reviews(request, event_id):
    try:
        if request.method == "POST":
            try:
                print(f"is_authenticated: {request.user.is_authenticated}")
                event = Event.objects.get(id=event_id)
                user = request.user
                review, created = Review.objects.get_or_create(
                    event = event,
                    user = user,
                    defaults={
                        "rating" : int(request.data.get("rating")),
                        "comment" : request.data.get("comment"),
                    }
                )
                if created:
                    review.save()
                    serializer = ReviewSerializer(review)

                    return Response(serializer.data)
                else:
                    return Response({"error": f"{user.username} already reviewed {event.title}"})
            except Exception as e:
                return Response({"error": f"{e}"})
        elif request.method == "GET":
            try:
                event = Event.objects.get(id = event_id)
                reviews = Review.objects.filter(event=event)
                serializer = ReviewSerializer(reviews, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": f"{e}"})
        else:
            raise Exception
    except Exception as e:
        return Response({"Error": f"{e}"})

# _________________________ XXXXXXXXXXXXXXXXXXX _________________________



# _______________________________ INVITES _______________________________
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def invite_users(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        # Only organizer can invite
        if request.user != event.organizer:
            return Response({"Unauthorized":"Only a organizer can invite to the event. And Unfortunatly you are not."})

        user_ids = request.data.get("user_ids", [])
        users = User.objects.filter(id__in=user_ids)

        for user in users:
            event.invited.add(user)

        return Response({"message": "Users invited successfully!"})
    except Exception as e:
        return Response({"error": str(e)})