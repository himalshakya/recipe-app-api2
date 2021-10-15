import pytest
from django.urls import reverse
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

TEST_EMAIL = 'test@testemail.com'
CREATE_PAYLOAD = {
    'email': TEST_EMAIL,
    'password': 'testpass',
    'name': 'Test name'
}


def create_user(django_user_model, **params):
    return django_user_model.objects.create_user(**params)


@pytest.mark.django_db
class TestPublicUserApi:
    """Test the user API (public)"""

    def test_create_valid_user_success(self, client, django_user_model):
        """Test creating user with valid payload is successful"""
        res = client.post(CREATE_USER_URL, CREATE_PAYLOAD)

        assert res.status_code == status.HTTP_201_CREATED

        user = django_user_model.objects.get(**res.data)
        assert user.check_password(CREATE_PAYLOAD['password'])
        assert 'password' not in res.data

    def test_user_exists(self, client, django_user_model):
        """Test creating a user that already exists fails"""
        create_user(django_user_model, **CREATE_PAYLOAD)

        res = client.post(CREATE_USER_URL, CREATE_PAYLOAD)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_short(self, client, django_user_model):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': TEST_EMAIL,
            'password': 'pw',
            'name': 'Test name'
        }
        res = client.post(CREATE_USER_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        user_exists = django_user_model.objects.filter(
            email=CREATE_PAYLOAD['email']
        ).exists()
        assert not user_exists

    def test_create_token_for_user(self, client, django_user_model):
        """Test that a token is created for the user"""
        create_user(django_user_model, **CREATE_PAYLOAD)
        res = client.post(TOKEN_URL, CREATE_PAYLOAD)

        assert 'token' in res.data
        assert res.status_code == status.HTTP_200_OK

    def test_create_token_invalid_credentials(self, client, django_user_model):
        """Test that token is not created if invalid credentials are given"""
        create_user(django_user_model, **CREATE_PAYLOAD)
        payload = {'email': TEST_EMAIL, 'password': 'wrong_password'}
        res = client.post(TOKEN_URL, payload)

        assert 'token' not in res.data
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_token_no_user(self, client):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'no_user', 'password': 'some_password'}
        res = client.post(TOKEN_URL, payload)

        assert 'token' not in res.data
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_token_missing_field(self, client):
        """Test that email and password are required"""
        res = client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        assert 'token' not in res.data
        assert res.status_code == status.HTTP_400_BAD_REQUEST
