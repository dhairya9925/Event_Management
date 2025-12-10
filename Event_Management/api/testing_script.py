import requests

API = "http://localhost:8000"

access = None
refresh = None


# ========================= AUTH =========================
def login(username="user", password="test"):
    global access, refresh

    url = f"{API}/api/token/"
    payload = {
        "username": "dhairya",
        "password": "Dhairya@995",
    }

    res = requests.post(url, json=payload)
    tokens = res.json()

    access = tokens.get("access")
    refresh = tokens.get("refresh")

    print("Logged in, access token:", access)
    return tokens


def auth_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access}",
    }


# ========================= EVENTS =========================

def create_event(data):
    url = f"{API}/event"
    res = requests.post(url, headers=auth_headers(), json=data)
    return res.json()


def list_events():
    url = f"{API}/event"
    res = requests.get(url, headers=auth_headers())
    return res.json()


def view_event(event_id):
    url = f"{API}/event/{event_id}"
    res = requests.get(url, headers=auth_headers())
    return res.json()


def update_event(event_id, data):
    url = f"{API}/event/{event_id}"
    res = requests.put(url, headers=auth_headers(), json=data)
    return res.json()


def delete_event(event_id):
    url = f"{API}/event/{event_id}"
    res = requests.delete(url, headers=auth_headers())
    return res.json()


# ========================= INVITES =========================

def invite_users(event_id, user_ids):
    url = f"{API}/event/{event_id}/invite"
    payload = {"user_ids": user_ids}
    res = requests.post(url, headers=auth_headers(), json=payload)
    return res.json()


# ========================= RSVP =========================

def create_rsvp(event_id, status):
    url = f"{API}/event/{event_id}/rsvp"
    payload = {"status": status}
    res = requests.post(url, headers=auth_headers(), json=payload)
    return res.json()


def update_rsvp(event_id, user_id, status):
    url = f"{API}/event/{event_id}/rsvp/{user_id}"
    payload = {"status": status}
    res = requests.patch(url, headers=auth_headers(), json=payload)
    return res.json()


# ========================= REVIEWS =========================

def add_review(event_id, rating, comment):
    url = f"{API}/event/{event_id}/reviews"
    payload = {
        "rating": rating,
        "comment": comment,
    }
    res = requests.post(url, headers=auth_headers(), json=payload)
    return res.json()


def list_reviews(event_id):
    url = f"{API}/event/{event_id}/reviews"
    res = requests.get(url, headers=auth_headers())
    return res.json()


# ========================= TEST RUN =========================
if __name__ == "__main__":
    login()

    print("\n--- Create Event ---")
    event = create_event({
        "title": "API Test Event",
        "description": "Testing event creation",
        "location": "Ahmedabad",
        "start_time": "12/12/2025 18:00",
        "end_time": "12/12/2025 20:00",
        "is_public": "yes"
    })
    print(event)

    event_id = event.get("id")

    print("\n--- List Events ---")
    print(list_events())

    print("\n--- View Event ---")
    print(view_event(event_id))

    print("\n--- Invite Users ---")
    print(invite_users(event_id, [1, 2]))

    print("\n--- Add Review ---")
    print(add_review(event_id, 5, "Great event!"))

    print("\n--- List Reviews ---")
    print(list_reviews(event_id))
