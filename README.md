# Event Management System API

A RESTful API built with Django and Django REST Framework for managing events, RSVPs, and reviews. Features JWT authentication, custom permissions, pagination, filtering, and search functionality.

## Features

- **Event Management**: Create, read, update, and delete events
- **RSVP System**: Users can RSVP to events with status options (Going, Maybe, Not Going)
- **Review System**: Users can leave reviews and ratings (1-5 stars) for events
- **Authentication**: JWT-based authentication for secure API access
- **Permissions**: Custom permissions for event organizers and private event access
- **Pagination**: Paginated responses for event and review listings
- **Search & Filter**: Search events by title, description, location, or organizer
- **Private Events**: Support for private events with invitation system

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository
`git clone https://github.com/dhairya9925/Event_Management
cd Event_Management`

### 2. Create and Activate Virtual Environment

**On Linux/Mac:**
`pip install uv 
uv venv
source .venv/bin/activate`


#### install dependencies
`uv synv` at root level where "pyproject.toml" is located 
or 
`pip install django djangorestframework djangorestframework-simplejwt django-cors-headers Pillow`

### Note
run testing_script.py to test not actual testcase but it gets you started
