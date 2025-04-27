# Health Information System

## Description
The Health Information System is a web-based application designed to help doctors manage health programs and client information. It allows users to:
- Create health programs (e.g., TB, Malaria, HIV).
- Register new clients in the system.
- Enroll clients in one or more health programs.
- Search for clients from a list of registered clients.
- View a client's profile, including the programs they are enrolled in.

This project is built using Django and Django REST Framework, with an API-first approach to ensure scalability and integration with other systems.

---

## Features
1. **Create Health Programs**: Add new health programs with a name and description.
2. **Register Clients**: Register clients with details such as name, age, gender, and contact information.
3. **Enroll Clients in Programs**: Enroll clients in one or more health programs.
4. **Search Clients**: Search for clients by name or contact information.
5. **View Client Profiles**: View detailed client profiles, including their enrolled programs.
6. **API Integration**: Expose client profiles and other functionalities via RESTful APIs.

---

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite
- **Other Tools**: 
  - `drf-yasg` for API documentation (Swagger UI)
  - `crispy-forms` for enhanced form rendering

---

## Setup Instructions
Follow these steps to set up the project on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd health-info-system

2. **Create a Virtual Environment**
   ```bash    
   python -m venv env
   source env/Scripts/activate #On Windows

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Run Migrations** 
   ```bash
   python manage.py migrate

5. **Start the Development Server**
   ```bash
   python manage.py runserver

6. **Access the Application** 
   [Open your browser and go to](http://127.0.0.1:8000)          
     