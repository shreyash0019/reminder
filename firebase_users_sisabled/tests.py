from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class FirebaseUsersTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_users_list(self):
        response = self.client.get(reverse("list_users"))
        self.assertEqual(response.status_code, 200)
