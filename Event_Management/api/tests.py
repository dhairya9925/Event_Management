# from django.test import TestCase
# import requests
# from models import User
# # Create your tests here.

# # urlpatterns = [
# #     path('', views.home),
# #     path('event', views.handle_event),
# #     path('event/<str:id>', views.handle_specified_event),
# #     path('event/<str:event_id>/invite', views.invite_users),
# #     path('event/<str:event_id>/rsvp', views.create_rsvp),
# #     path('event/<str:event_id>/rsvp/<str:user_id>', views.update_rsvp),
# #     path('event/<str:id>/reviews', views.handle_reviews),
# #     # path('delete/<str:id>', views.delete_event),
# # ]

# BASE_URL = "http://localhost:8000/api/token/"
# access = ...
# refresh = ...
# csrftoken = ...

# def login():
#     # username = input("Enter username:")
#     # password = input("Enter Password:")
#     json={
#         "username": "dhairya",
#         "password": "Dhairya@995",
#     },
#     headers={
#         "Content-Type": "application/json"
#     },

#     res = requests.post(
#         url = BASE_URL,
#         json=json,
#         headers=headers,
#     )

#     access = res.json()['access']
#     refresh = res.json()['refresh']
#     # print(res.json()['access'])
#     return res.json()

# def create_event():
#     url = f"{BASE_URL}/event"
#     headers={
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access}",
#     },
#     data={
#         "title": input("Event title: "),
#         "description": input("Event description: "),
#         "organizer": "",
#         "location": input("Event location: "),
#         "start_time": input("Event start_time(dd/mm/yyyy hh:mm): "),
#         "end_time": input("Event end_time(dd/mm/yyyy hh:mm): "),
#         "is_public": input("Is Event Public (y or yes for public event): "),
#     }
    
#     res = requests.post(
#         url=url,
#         headers=headers,
#         json=data,
#     )

#     return res.json()


# def view_events():
#     url = f"{BASE_URL}/event"
#     headers={
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access}",
#     },
#     # data={}
    
#     res = requests.post(
#         url=url,
#         headers=headers,
#         # json=data,
#     )

#     return res.json()


# def invite():
#     url = f"{BASE_URL}/event"
#     headers={
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access}",
#     },

#     print("Leave blank to exit")
#     count = 0
#     guest_list = []
#     while(True):
#         count += 1
#         guest = input(f"Enter guest {count}:")
#         if guest == "":
#             break
#         guest_list.append(guest)

#     guest_ids = []
#     outliers = []
#     for guest in guest_list:
#         try:
#             user = User.objects.get(username=guest)
#             # user_p = user
#             guest_ids.append(user.id)
#         except User.DoesNotExist as e:
#             outliers.append(user.username)
    
#     print("Guests Invited")
#     for idx, _guest in enumerate(guest_list):
#         print(f"{idx}. {_guest}", end="\t")
#     print()
        
#     print("Following guests in db Does Not exist")
#     for idx, outlier in enumerate(outliers):
#         print(f"{idx}. {outlier}", end="\t")

#     data={
#         "user_ids": guest_ids
#     }
    
#     res = requests.post(
#         url=url,
#         headers=headers,
#         json=data,
#     )

#     return res.json()


#     # print(res.headers.get('refresh'))
#     # print(res.__dict__['refresh'])


# def view_event(event_id):
#     access = login()['access']
#     url = f"{BASE_URL}/event/{event_id}"
#     headers={
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access}",
#     },
#     # data={}
    
#     res = requests.post(
#         url=url,
#         headers=headers,
#         # json=data,
#     )

#     return res.json()



# def update_event():
#     url = f"{BASE_URL}/event"
#     headers={
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access}",
#     },
#     # data={}
    
#     res = requests.post(
#         url=url,
#         headers=headers,
#         # json=data,
#     )

#     return res.json()



# def delete_event():
#     url = f"{BASE_URL}/event"
#     headers={
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access}",
#     },
#     # data={}
    
#     res = requests.post(
#         url=url,
#         headers=headers,
#         # json=data,
#     )

#     return res.json()





# # def event_management():


# if __name__ == "__main__":
#     view_event(2)

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import Event, Review, RSVP, UserProfile


class EventAPITestCase(TestCase):
    """Test cases for Event API endpoints"""
    
    def setUp(self):
        """Set up test data before each test"""
        self.client = APIClient()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Create user profiles
        self.profile1 = UserProfile.objects.create(
            user=self.user1,
            full_name='Test User 1'
        )
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            full_name='Test User 2'
        )
        
        # Create test events
        self.public_event = Event.objects.create(
            title='Public Test Event',
            description='A public event for testing',
            organizer=self.user1,
            location='Test Location',
            start_time=datetime.now() + timedelta(days=1),
            end_time=datetime.now() + timedelta(days=1, hours=2),
            is_public=True
        )
        
        self.private_event = Event.objects.create(
            title='Private Test Event',
            description='A private event for testing',
            organizer=self.user1,
            location='Private Location',
            start_time=datetime.now() + timedelta(days=2),
            end_time=datetime.now() + timedelta(days=2, hours=2),
            is_public=False
        )
        self.private_event.invited.add(self.user1)


class HomeViewTests(EventAPITestCase):
    """Test cases for home endpoint"""
    
    def test_home_endpoint(self):
        """Test that home endpoint returns healthy status"""
        response = self.client.get('/api/home/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['fittness'], 'Healthy')


class HandleEventTests(EventAPITestCase):
    """Test cases for handle_event view (GET and POST)"""
    
    def test_get_events_unauthenticated(self):
        """Test that unauthenticated users cannot view events"""
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_events_authenticated(self):
        """Test that authenticated users can view their accessible events"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_events_shows_public_events(self):
        """Test that public events are visible to all authenticated users"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that public event is in response
        event_titles = [event['title'] for event in response.data]
        self.assertIn('Public Test Event', event_titles)
    
    def test_get_events_hides_private_events_from_non_invited(self):
        """Test that private events are hidden from non-invited users"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/events/')
        
        event_titles = [event['title'] for event in response.data]
        self.assertNotIn('Private Test Event', event_titles)
    
    def test_get_events_shows_private_events_to_invited(self):
        """Test that private events are visible to invited users"""
        self.private_event.invited.add(self.user2)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/events/')
        
        event_titles = [event['title'] for event in response.data]
        self.assertIn('Private Test Event', event_titles)
    
    def test_create_event_unauthenticated(self):
        """Test that unauthenticated users cannot create events"""
        event_data = {
            'title': 'New Event',
            'description': 'Event description',
            'location': 'Test Location',
            'start_time': '15/12/2025 10:00',
            'end_time': '15/12/2025 12:00',
            'is_public': 'yes'
        }
        response = self.client.post('/api/events/', event_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_public_event(self):
        """Test creating a public event"""
        self.client.force_authenticate(user=self.user1)
        event_data = {
            'title': 'New Public Event',
            'description': 'Public event description',
            'location': 'Public Location',
            'start_time': '20/12/2025 14:00',
            'end_time': '20/12/2025 16:00',
            'is_public': 'yes'
        }
        response = self.client.post('/api/events/', event_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'New Public Event')
        self.assertTrue(response.data['is_public'])
    
    def test_create_private_event(self):
        """Test creating a private event"""
        self.client.force_authenticate(user=self.user1)
        event_data = {
            'title': 'New Private Event',
            'description': 'Private event description',
            'location': 'Private Location',
            'start_time': '21/12/2025 14:00',
            'end_time': '21/12/2025 16:00',
            'is_public': 'no'
        }
        response = self.client.post('/api/events/', event_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_public'])
        
        # Check that organizer is automatically invited to private event
        event = Event.objects.get(id=response.data['id'])
        self.assertIn(self.user1, event.invited.all())


class ViewEventTests(EventAPITestCase):
    """Test cases for view_event endpoint"""
    
    def test_view_existing_event(self):
        """Test viewing a specific event by ID"""
        response = self.client.get(f'/api/events/{self.public_event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Public Test Event')
    
    def test_view_nonexistent_event(self):
        """Test viewing a non-existent event returns error"""
        response = self.client.get('/api/events/99999/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Error', response.data)


class UpdateEventTests(EventAPITestCase):
    """Test cases for update_event endpoint"""
    
    def test_update_event_as_organizer(self):
        """Test that organizer can update their event"""
        self.client.force_authenticate(user=self.user1)
        update_data = {
            'title': 'Updated Event Title',
            'description': 'Updated description',
            'location': 'Updated Location',
            'start_time': '25/12/2025 10:00',
            'end_time': '25/12/2025 12:00',
            'is_public': True
        }
        response = self.client.put(f'/api/events/{self.public_event.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_event_as_non_organizer(self):
        """Test that non-organizer cannot update event"""
        self.client.force_authenticate(user=self.user2)
        update_data = {
            'title': 'Unauthorized Update',
            'description': 'Should not work',
            'location': 'Test',
            'start_time': '25/12/2025 10:00',
            'end_time': '25/12/2025 12:00',
            'is_public': True
        }
        response = self.client.put(f'/api/events/{self.public_event.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Unauthorized', response.data)


class DeleteEventTests(EventAPITestCase):
    """Test cases for delete_event endpoint"""
    
    def test_delete_event(self):
        """Test deleting an event"""
        event = Event.objects.create(
            title='Event to Delete',
            description='Will be deleted',
            organizer=self.user1,
            location='Test',
            start_time=datetime.now() + timedelta(days=3),
            end_time=datetime.now() + timedelta(days=3, hours=2),
            is_public=True
        )
        response = self.client.delete(f'/api/events/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify event is deleted
        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(id=event.id)


class RSVPTests(EventAPITestCase):
    """Test cases for RSVP endpoints"""
    
    def test_create_rsvp(self):
        """Test creating an RSVP"""
        self.client.force_authenticate(user=self.user1)
        rsvp_data = {'status': 'attending'}
        response = self.client.post(
            f'/api/events/{self.public_event.id}/rsvp/',
            rsvp_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_duplicate_rsvp(self):
        """Test that duplicate RSVPs are prevented"""
        self.client.force_authenticate(user=self.user1)
        
        # Create first RSVP
        RSVP.objects.create(
            event=self.public_event,
            user=self.profile1,
            status='attending'
        )
        
        # Try to create duplicate
        rsvp_data = {'status': 'attending'}
        response = self.client.post(
            f'/api/events/{self.public_event.id}/rsvp/',
            rsvp_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Already Exist', response.data['message'])


class ReviewTests(EventAPITestCase):
    """Test cases for review endpoints"""
    
    def test_add_review_unauthenticated(self):
        """Test that unauthenticated users cannot add reviews"""
        review_data = {
            'rating': 5,
            'comment': 'Great event!'
        }
        response = self.client.post(
            f'/api/events/{self.public_event.id}/reviews/',
            review_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_review_authenticated(self):
        """Test adding a review as authenticated user"""
        self.client.force_authenticate(user=self.user1)
        review_data = {
            'rating': 4,
            'comment': 'Nice event!'
        }
        response = self.client.post(
            f'/api/events/{self.public_event.id}/reviews/',
            review_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4)
    
    def test_add_duplicate_review(self):
        """Test that users cannot review the same event twice"""
        self.client.force_authenticate(user=self.user1)
        
        # Create first review
        Review.objects.create(
            event=self.public_event,
            user=self.profile1,
            rating=5,
            comment='First review'
        )
        
        # Try to create duplicate
        review_data = {
            'rating': 4,
            'comment': 'Second review'
        }
        response = self.client.post(
            f'/api/events/{self.public_event.id}/reviews/',
            review_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('already reviewed', response.data['error'])
    
    def test_get_reviews_for_event(self):
        """Test retrieving all reviews for an event"""
        self.client.force_authenticate(user=self.user1)
        
        # Create some reviews
        Review.objects.create(
            event=self.public_event,
            user=self.profile1,
            rating=5,
            comment='Great!'
        )
        Review.objects.create(
            event=self.public_event,
            user=self.profile2,
            rating=4,
            comment='Good!'
        )
        
        response = self.client.get(f'/api/events/{self.public_event.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class InviteUsersTests(EventAPITestCase):
    """Test cases for invite_users endpoint"""
    
    def test_invite_users_as_organizer(self):
        """Test that organizer can invite users to event"""
        self.client.force_authenticate(user=self.user1)
        invite_data = {
            'user_ids': [self.user2.id]
        }
        response = self.client.post(
            f'/api/events/{self.private_event.id}/invite/',
            invite_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('invited successfully', response.data['message'])
        
        # Verify user was invited
        self.assertIn(self.user2, self.private_event.invited.all())
    
    def test_invite_users_as_non_organizer(self):
        """Test that non-organizer cannot invite users"""
        self.client.force_authenticate(user=self.user2)
        invite_data = {
            'user_ids': [self.user2.id]
        }
        response = self.client.post(
            f'/api/events/{self.private_event.id}/invite/',
            invite_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Unauthorized', response.data)
    
    def test_invite_multiple_users(self):
        """Test inviting multiple users at once"""
        self.client.force_authenticate(user=self.user1)
        
        # Create additional users
        user3 = User.objects.create_user(
            username='testuser3',
            password='testpass123'
        )
        user4 = User.objects.create_user(
            username='testuser4',
            password='testpass123'
        )
        
        invite_data = {
            'user_ids': [self.user2.id, user3.id, user4.id]
        }
        response = self.client.post(
            f'/api/events/{self.private_event.id}/invite/',
            invite_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all users were invited
        self.assertEqual(self.private_event.invited.count(), 4)  # Including organizer