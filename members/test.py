from django.test import TestCase

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
                
    
