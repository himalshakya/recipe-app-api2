import pytest


def test_create_user_with_email_successful(django_user_model):
    """
      Test creating a new user with an email is successful
    """
    email = 'test_user@test.com'
    password = 'TestPassword123'
    user = django_user_model.objects.create_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)


def test_new_user_email_normalized(django_user_model):
    """Test the email for a new user is normalized"""
    email = 'test@TEST_EMAIL.COM'
    user = django_user_model.objects.create_user(email=email, password='TestPassword123')

    assert user.email == email.lower(), "email has not been normalized"


def test_new_user_invalid_email(django_user_model):
    """Test creating user with no email raises error"""
    with pytest.raises(ValueError):
        django_user_model.objects.create_user(email=None, password='TestPassword123')


def test_create_new_superuser(django_user_model):
    """Test creating a new superuser"""
    user = django_user_model.objects.create_superuser('test_user@test.com', 'TestPassword123')

    assert user.is_superuser, "User not set to superuser"
    assert user.is_staff, "User not set to staff"
