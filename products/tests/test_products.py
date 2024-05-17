from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from categories.models import Category
from products.models import Product


class ProductCRUDTestCase(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(email='1@1.com', password='1', username='1')
        self.user2 = get_user_model().objects.create_user(email='2@2.com', password='2', username='2')
        self.admin = get_user_model().objects.create_superuser(email='3@3.com', password='3', username='3')
        self.total_users = 3

        self.category1 = Category.objects.create(name='category1')

        self.total_products = 0

    def test_create_product(self):
        data = {
            'name': 'product1',
            'price': '100',
            'discount': '50.00',
            'quantity': 10,
            'description': 'description1',
            'category': 1,
        }
        self.client.force_login(self.user1)
        url = reverse('products-list')
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), self.total_products + 1)
        self.assertEqual(Product.objects.last().owner, self.user1)
