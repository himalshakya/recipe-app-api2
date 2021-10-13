from django.urls import reverse
import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user_super(client, django_user_model):
    super_user = django_user_model.objects.create_superuser(
        email='admin@test.com',
        password='password123'
    )
    client.force_login(super_user)
    return super_user


@pytest.fixture
def user_normal(django_user_model) -> User:
    return django_user_model.objects.create_user(
        email='test@test.com',
        password='password123',
        name='Test User'
    )


def test_users_listed(client, user_super, user_normal):
    """Test that users are listed on user page"""
    url = reverse('admin:core_user_changelist')
    res = client.get(url)

    assert user_super.email in str(res.content)
    assert user_normal.name in str(res.content)
    assert user_normal.email in str(res.content)


def test_user_change_page(client, user_normal):
    """Test that the user edit page works"""
    url = reverse('admin:core_user_change', args=[user_normal.id])
    res = client.get(url, follow=True)

    assert res.status_code == 200


def test_create_user_page(client):
    """Test that the create user page works"""
    url = reverse('admin:core_user_add')
    res = client.get(url, follow=True)

    assert res.status_code == 200
