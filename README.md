# Event Management System API

A RESTful API built with Django and Django REST Framework for managing events, RSVPs, and reviews. Features JWT authentication, custom permissions, and support for private events with invitations.

## Features

- **Event Management**: Create, read, update, and delete events
- **RSVP System**: Users can RSVP to events with status options (Going, Maybe, Not Going)
- **Review System**: Users can leave reviews and ratings (1-5 stars) for events
- **Authentication**: JWT-based authentication for secure API access
- **Permissions**: Organizer-only permissions for event modification
- **Private Events**: Support for private events with invitation system
- **User Profiles**: Extended user profiles with bio, location, and profile picture

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository
```
git clone https://github.com/dhairya9925/Event_Management

cd Event_Management
```

### 2. Create and Activate Virtual Environment

#### Using `uv`

**On Linux/Mac:**

```
pip install uv

uv venv

source .venv/bin/activate
```

**On Windows:**

```
pip install uv

uv venv

.venv\Scripts\activate

```


**install dependencies**: 
`uv synv` at root level where "pyproject.toml" is located 

#### Using `virtualvenv`
```
pip install virtualvenv

python -m venv .venv

source .venv/bin/activate  # linux/mac

.venv/Scripts/activate  # Windows

cd Event_Management

```

**install dependencies**: 
`pip install django djangorestframework djangorestframework-simplejwt django-cors-headers Pillow`


### 3. Apply Migrations and Create Superuser

```
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
```

### Note:
- Functionality can be tested through the Django Admin interface as well
- You may create and manage users directly from the Django Admin interface or via custom scripts.

  *_only users in auth_user in db can login._  

- Use `api/testing_script.py` for initial testing. 
  This script is not a formal test suite, but helps verify core functionality.
