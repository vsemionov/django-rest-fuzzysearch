from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


user = User.objects.create(username='test', password='test')


class TestUsers(APITestCase):

    base_url = reverse('user-list')

    def test_list_success(self):
        response = self.client.get(self.base_url + '?search=' + user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
