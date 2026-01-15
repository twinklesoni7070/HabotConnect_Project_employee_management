from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Employee

class EmployeeAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass12345")

        token_resp = self.client.post(
            "/api/token/",
            {"username": "tester", "password": "pass12345"},
            format="json",
        )
        assert token_resp.status_code == status.HTTP_200_OK
        access = token_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_create_employee_success(self):
        resp = self.client.post("/api/employees/", {
            "name": "Alice",
            "email": "alice@example.com",
            "department": "Engineering",
            "role": "Developer"
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_employee_duplicate_email(self):
        Employee.objects.create(name="Bob", email="bob@example.com")
        resp = self.client.post("/api/employees/", {
            "name": "Bobby",
            "email": "bob@example.com"
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_pagination_and_filter(self):
        for i in range(12):
            Employee.objects.create(
                name=f"Emp {i}",
                email=f"e{i}@example.com",
                department="HR" if i % 2 == 0 else "Engineering",
                role="Developer" if i % 3 == 0 else "Analyst",
            )

        page1 = self.client.get("/api/employees/")
        self.assertEqual(page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(page1.data["results"]), 10)

        page2 = self.client.get("/api/employees/?page=2")
        self.assertEqual(page2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(page2.data["results"]), 2)

        filtered = self.client.get("/api/employees/?department=HR")
        self.assertEqual(filtered.status_code, status.HTTP_200_OK)
        for item in filtered.data["results"]:
            self.assertEqual(item["department"], "HR")

    def test_retrieve_update_delete(self):
        emp = Employee.objects.create(name="Carol", email="carol@example.com")

        get_resp = self.client.get(f"/api/employees/{emp.id}/")
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)

        put_resp = self.client.put(f"/api/employees/{emp.id}/", {
            "name": "Carol Updated",
            "email": "carol@example.com",
            "department": "Sales",
            "role": "Manager"
        }, format="json")
        self.assertEqual(put_resp.status_code, status.HTTP_200_OK)

        del_resp = self.client.delete(f"/api/employees/{emp.id}/")
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_blocked(self):
        self.client.credentials()  # remove token
        resp = self.client.get("/api/employees/")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
