from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class TestUsers(APITestCase):

    def test_list_success(self):
        user = User.objects.create(username='test', password='test')

        base_url = reverse('user-list')

        response = self.client.get(base_url + '?search=' + user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
