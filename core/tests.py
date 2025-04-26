from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Client, HealthProgram, Enrollment

# Create your tests here.
#Test for Creating a Health Program
class HealthProgramAPITestCase(APITestCase):
    def test_create_health_program(self):
        data = {
            "name": "Malaria",
            "description": "Eradicate Malaria"
        }
        response = self.client.post('/api/create-program/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Malaria")

# Test for Registering a Client
class ClientAPITestCase(APITestCase):
    def test_register_client(self):
        data = {
            "name": "John Doe",
            "age": 30,
            "gender": "M",
            "contact": "1234567890"
        }
        response = self.client.post('/api/register-client/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "John Doe")

#Test for Enrolling a Client in Programs
class EnrollmentAPITestCase(APITestCase):
    def setUp(self):
        # Create a client and health programs
        self.client_obj = Client.objects.create(name="Jane Doe", age=25, gender="F", contact="0987654321")
        self.program1 = HealthProgram.objects.create(name="HIV", description="HIV Awareness")
        self.program2 = HealthProgram.objects.create(name="TB", description="TB Campaign")

    def test_enroll_client(self):
        # Pass both program IDs in the request
        data = {
            "client_id": self.client_obj.id,
            "program_ids": [self.program1.id, self.program2.id]  # Include both program IDs
        }
        print(f"Test Data: {data}")  # Debug statement to verify the test data
        response = self.client.post('/api/enroll-client/', data, format='json')  # Ensure format is JSON
        
        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that two enrollments were created
        self.assertEqual(Enrollment.objects.filter(client=self.client_obj).count(), 2)
        
# Test for Searching Clients
class SearchClientsAPITestCase(APITestCase):
    def setUp(self):
        # Create some clients
        Client.objects.create(name="Alice", age=28, gender="F", contact="0714578890")
        Client.objects.create(name="Bob", age=35, gender="M", contact="0736456789")

    def test_search_clients(self):
        response = self.client.get('/api/search-clients/?q=Alice')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Alice")                      


#Test for Retrieving a Client Profile
class ClientProfileAPITestCase(APITestCase):
    def setUp(self):
        # Create a client and enroll them in a program
        self.client_obj = Client.objects.create(name="Charlie", age=40, gender="M", contact="0712345768")
        self.program = HealthProgram.objects.create(name="Malaria", description="Malaria Eradication")
        Enrollment.objects.create(client=self.client_obj, program=self.program)

    def test_client_profile(self):
        response = self.client.get(f'/api/client/{self.client_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Charlie")
        self.assertEqual(len(response.data['enrollments']), 1)
        self.assertEqual(response.data['enrollments'][0]['program']['name'], "Malaria")        