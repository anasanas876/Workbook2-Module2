from rest_framework.test import APITestCase
from django.urls import reverse

from .models import Company, User, Project, Task


class TenantIsolationTest(APITestCase):

    def setUp(self):
        # Create companies
        self.company_a = Company.objects.create(name="Google")
        self.company_b = Company.objects.create(name="Microsoft")

        # Create users
        self.user_a = User.objects.create_user(
            username="user_a",
            password="12345",
            company=self.company_a,
            role="employee"
        )

        self.user_b = User.objects.create_user(
            username="user_b",
            password="12345",
            company=self.company_b,
            role="employee"
        )

        # Create projects
        self.project_a = Project.objects.create(
            name="Website",
            description="Company A Project",
            start_date=1,
            status="NS"
        )

        self.project_b = Project.objects.create(
            name="Payroll",
            description="Company B Project",
            start_date=1,
            status="NS"
        )

        # Create tasks
        Task.objects.create(
            project=self.project_a,
            company=self.company_a,
            name="Build Website",
            description="Frontend",
            start_date=1,
            status="NS"
        )

        Task.objects.create(
            project=self.project_b,
            company=self.company_b,
            name="Payroll System",
            description="Backend",
            start_date=1,
            status="NS"
        )

    def test_company_a_cannot_access_company_b_tasks(self):

        # Login as User A
        self.client.force_authenticate(user=self.user_a)

        # Call API
        response = self.client.get(reverse("get_task"))

        # Response should be successful
        self.assertEqual(response.status_code, 200)

        # Every returned task must belong to Company A
        for task in response.data["data"]:
            self.assertEqual(task["company"], self.user_a.company.id)

        # No returned task should belong to Company B
        for task in response.data["data"]:
            self.assertNotEqual(task["company"], self.user_b.company.id)