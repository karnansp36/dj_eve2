from django.db import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse

from .models import UserModel


class UserModelTests(APITestCase):
    def test_usermodel_str(self):
        user = UserModel.objects.create(
            username='alice', email='alice@example.com', password='pass123'
        )
        self.assertEqual(str(user), 'alice')

    def test_unique_username_constraint(self):
        UserModel.objects.create(username='bob', email='bob1@example.com', password='p')
        with self.assertRaises(IntegrityError):
            # creating a second user with same username should raise an integrity error
            UserModel.objects.create(username='bob', email='bob2@example.com', password='p')


class UserViewsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = '/api/users/'

    def test_get_user_list(self):
        UserModel.objects.create(username='u1', email='u1@example.com', password='p')
        UserModel.objects.create(username='u2', email='u2@example.com', password='p')
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_create_user_via_post(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass',
            'first_name': 'New',
            'last_name': 'User'
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserModel.objects.filter(username='newuser').exists())

    def test_user_detail_get_put_delete(self):
        user = UserModel.objects.create(username='detail', email='d@example.com', password='p')
        detail_url = f'/api/users/{user.id}/'

        # GET
        resp_get = self.client.get(detail_url)
        self.assertEqual(resp_get.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_get.data['username'], 'detail')

        # PUT
        update_payload = {'username': 'detail2', 'email': 'd2@example.com', 'password': 'p', 'first_name': 'F', 'last_name': 'L'}
        resp_put = self.client.put(detail_url, update_payload, format='json')
        self.assertEqual(resp_put.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_put.data['username'], 'detail2')

        # DELETE
        resp_delete = self.client.delete(detail_url)
        self.assertEqual(resp_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserModel.objects.filter(pk=user.id).exists())

    def test_protected_view_requires_auth(self):
        prot_url = '/api/protected/'
        # unauthenticated should be 401
        resp = self.client.get(prot_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_view_with_authenticated_user(self):
        prot_url = '/api/protected/'
        # create a Django auth user and force authenticate
        django_user = User.objects.create_user(username='authuser', password='secret')
        self.client.force_authenticate(user=django_user)
        resp = self.client.get(prot_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('message'), 'This is a protected view!')
