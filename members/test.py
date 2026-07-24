from django.test import TestCase
from rest_framework.test import APITestCase

from .models import User,Company,Project
class TenantTestCase(TestCase):


    def setUp(self):
        company1 = Company.objects.create(company_name="A")
        company2 = Company.objects.create(company_name="B")
        project1=Project.objects.create(name="Web Development",description="Create a website",start_date=5,status="IP",company_projects=company1)
        project2=Project.objects.create(name="App Development",description="Create an App",start_date=5,status="IP",company_projects=company2)
        self.user1=User.objects.create_user(username="jawad",password="123456789",role="employee",company=company1)
        self.user2=User.objects.create_user(username="rameez",password="123456789",role="employee",company=company2)
    def test_company_tenant(self):
        response=self.client.post("/login/",data={"username":"jawad",
                      "password":"123456789"})
        access=response.json()["access"]
        self.assertEqual(response.status_code,200)
        response_for_tenant=self.client.get("/specificprojects/",HTTP_AUTHORIZATION=f"Bearer {access}")
        verify=response_for_tenant.json()["data"]
        self.assertEqual(response_for_tenant.status_code, 200)
        # Making Sure API returns related  Projects
        self.assertGreater(len(verify), 0)
        for verification in verify:
            self.assertEqual (verification["company_projects"],self.user1.company.id)

# Writing Unit Test for Login Endpoint

class LoginTest(TestCase):
    def setUp(self):
        self.login_endpoint="/login/"
        self.data={"username":"ali",
              "password":"123456789"}
    def test_login(self):
        response=self.client.post(self.login_endpoint,self.data)
        self.assertEqual(response.status_code,200)

# Writing Unit Test For Signup endpoint
class SignupTest(TestCase):
    def setUp(self):
        self.signup_endpoint="/signup/"
        self.data={"username":"huraira",
               "password":"123456789",
               "role":"employee",
               "company":"G"}
    def test_signup(self):
        response=self.client.post(self.signup_endpoint,self.data)
        self.assertEqual(response.status_code, 201)

# Wriing ApI Test For Authorization
class CheckAuthorization(APITestCase):

    def setUp(self):
        login_request = self.client.post(
            "/login/",
            {
                "username": "ali",
                "password": "123456789"
            }
        )

        token = login_request.json()["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_admin_specific_projects(self):
        response = self.client.get("/projects/2/")

        self.assertEqual(response.status_code, 403)
