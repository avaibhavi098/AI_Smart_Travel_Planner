# ✈️ AI Smart Travel Planner

An AI-powered travel planning platform that helps users create personalized trips, manage destinations, optimize routes, generate AI-based itineraries, visualize journeys on interactive maps, and receive travel recommendations based on preferences.

---

# 📌 Project Overview

Planning a trip manually requires searching destinations, calculating routes, estimating budgets, finding activities, and organizing schedules.

AI Smart Travel Planner solves this problem by combining:

- Artificial Intelligence
- Maps and Location Services
- Route Optimization
- Personalized Recommendations
- Automated Itinerary Generation

Users can create trips, add destinations, visualize routes, and generate complete travel plans using AI.

---

# 🎯 Problem Statement

Traditional travel planning requires users to collect information from multiple platforms:

- Places to visit
- Route planning
- Travel duration
- Budget estimation
- Food preferences
- Activities

This process is time-consuming and difficult to personalize.

---

# 💡 Solution

AI Smart Travel Planner provides a single platform where users can:

- Create travel plans
- Add multiple destinations
- Calculate travel distance and duration
- View routes on maps
- Generate AI-powered itineraries
- Receive personalized travel suggestions
- Export and share travel plans

---

# 🚀 Features

## 🔐 Authentication

- User registration
- Email verification
- Secure login/logout
- Password reset using OTP
- User profile management


---

# 🌍 Trip Management

Users can:

- Create trips
- Edit trips
- Delete trips
- View previous trips

Trip details include:

- Trip name
- Source location
- Travel dates
- Budget
- Number of travelers
- Transport preference
- Travel style
- Food preference
- Interests


---

# 📍 Destination Management

Users can:

- Add destinations
- Edit destinations
- Delete destinations
- Reorder destinations

Each destination stores:

- City
- State
- Country
- Latitude
- Longitude
- Distance from previous location
- Travel duration


---

# 🗺️ Interactive Maps

Integrated map features:

- Destination markers
- Source location marker
- Route visualization
- Location details popup

Technology:

- Leaflet.js
- OpenStreetMap


---

# 🚦 Route Optimization

The system provides:

- Optimized travel sequence
- Total distance calculation
- Estimated travel time
- Route visualization

---

# 🤖 AI Itinerary Generator

The AI module generates:

- Day-wise travel plans
- Morning activities
- Afternoon activities
- Evening activities
- Food recommendations
- Estimated expenses
- Travel tips
- Packing checklist


AI Model:

```
Groq API
Llama 3.3 70B
```

---

# 📧 Email Features

The application sends:

- Account verification emails
- Password reset emails
- AI itinerary emails


Email features:

- HTML responsive templates
- PDF itinerary attachment


---

# 📄 PDF Export

Users can download:

- Complete itinerary PDF
- Trip details
- Budget summary
- Travel checklist


---

# 🏗️ Tech Stack


## Backend

- Python
- Django 6
- Django ORM
- SQLite


## Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript


## AI

- Groq API
- Llama 3.3 70B


## Maps

- Leaflet.js
- OpenStreetMap


## External Services

- Geoapify API
- Gmail SMTP


---

# 📂 Project Structure


```
AI_Smart_Travel_Planner

│
├── accounts
│   ├── authentication
│   ├── email verification
│   └── password reset
│
├── trips
│   ├── trip creation
│   ├── trip management
│   └── trip details
│
├── destinations
│   ├── destination management
│   └── location services
│
├── routes_app
│   └── route optimization
│
├── ai
│   ├── AI itinerary generation
│   └── Groq integration
│
├── assistant_ai
│   └── travel assistant
│
├── export_app
│   └── PDF generation
│
├── templates
│
├── static
│
├── media
│
├── manage.py
│
└── requirements.txt

```

---

# ⚙️ Installation Guide

## 1. Clone Repository


```bash
git clone <repository-url>
```


Move into project:

```bash
cd AI_Smart_Travel_Planner
```


---

# 2. Create Virtual Environment


Windows:


```bash
python -m venv venv
```


Activate:


```bash
venv\Scripts\activate
```


---

# 3. Install Dependencies


```bash
pip install -r requirements.txt
```


---

# 4. Environment Variables


Create:

```
.env
```


Add:


```
SECRET_KEY=your_secret_key

GROQ_API_KEY=your_groq_api_key

GEOAPIFY_API_KEY=your_geoapify_key

EMAIL_HOST_USER=your_email

EMAIL_HOST_PASSWORD=your_app_password

```


---

# 5. Database Setup


Run migrations:


```bash
python manage.py makemigrations

python manage.py migrate
```


---

# 6. Create Admin User


```bash
python manage.py createsuperuser
```


Enter:

```
Username
Email
Password
```


---

# ▶️ Running Project


Start Django server:


```bash
python manage.py runserver
```


Open:


```
http://127.0.0.1:8000/
```


---

# 🔄 Application Workflow


## Step 1: Register User

User creates an account.

↓

Verification email is sent.

↓

Account becomes active after verification.


---

## Step 2: Create Trip

User enters:

- Source location
- Travel dates
- Budget
- Preferences


↓

Trip is saved.


---

## Step 3: Add Destinations


User adds places:

Example:

```
Hyderabad
Goa
Mumbai
```


↓

Coordinates are fetched using Geoapify.


---

## Step 4: View Map


System displays:

- Source
- Destinations
- Route


---

## Step 5: Generate AI Itinerary


User clicks:

```
Generate AI Itinerary
```


↓

Groq AI generates:

- Complete schedule
- Expenses
- Travel tips


---

## Step 6: Email & PDF


User receives:

- AI itinerary email
- PDF attachment


---

# 🛡️ Error Handling

Implemented custom pages:

```
400 Bad Request

403 Permission Denied

404 Page Not Found

500 Server Error
```


---

# 🔒 Security Features

Implemented:

- Django authentication
- CSRF protection
- User based data access
- Password hashing
- Environment variables
- Secure email verification


---

# 🧪 Testing


Run Django checks:


```bash
python manage.py check
```


Run server:


```bash
python manage.py runserver
```


---

# 📦 Requirements Freeze


Dependencies are stored in:


```
requirements.txt
```


Update:


```bash
pip freeze > requirements.txt
```


---

# 🔮 Future Enhancements

- Real-time weather integration
- Hotel recommendations
- Flight booking integration
- Mobile application
- Voice travel assistant
- Social trip sharing
- Advanced AI recommendations


---

# 👨‍💻 Developer

AI Smart Travel Planner

Built using:

Python + Django + AI + Maps

---

# ❤️ Conclusion

AI Smart Travel Planner makes travel planning easier by combining AI intelligence, personalized recommendations, and interactive mapping into one complete travel management platform.