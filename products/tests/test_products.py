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
        self.category2 = Category.objects.create(name='category2')

        self.product1 = Product.objects.create(
            name='product1',
            price=123,
            discount=100,
            quantity=10,
            description='description1',
            category=self.category1,
            owner=self.user1,
        )
        self.product2 = Product.objects.create(
            name='product2',
            price=2,
            discount=1,
            quantity=1,
            description='description2',
            category=self.category1,
            owner=self.user2,
        )
        self.product1.save()
        self.product2.save()

        self.total_products = 2

    def test_create_product(self):
        data = {
            'name': 'product1',
            'price': '100',
            'discount': '50.00',
            'quantity': 10,
            'description': 'description1',
            'category': self.category1.id,
        }
        self.client.force_login(self.user1)
        url = reverse('products-list')
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), self.total_products + 1)
        self.assertEqual(Product.objects.last().owner, self.user1)

    def test_list_products(self):
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.total_products)

    def test_delete_product(self):
        self.client.force_login(self.user1)
        url = reverse('products-detail', args=[self.product1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), self.total_products - 1)

    def test_delete_product_not_owner(self):
        self.client.force_login(self.user1)
        url = reverse('products-detail', args=[self.product2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), self.total_products)

    def test_update_product(self):
        data = {
            'name': 'change_product1',
            'price': '1000',
            'discount': '500.00',
            'quantity': 100,
            'description': 'change_description1',
            'category': self.category2.id,
        }
        self.client.force_login(self.user1)
        self.product1.refresh_from_db()
        url = reverse('products-detail', args=[self.product1.id])
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), self.total_products)

        change_product = Product.objects.get(id=self.product1.id)
        self.assertEqual(change_product.name, 'change_product1')
        self.assertEqual(change_product.price, 1000)
        self.assertEqual(change_product.discount, 500.00)
        self.assertEqual(change_product.quantity, 100)
        self.assertEqual(change_product.description, 'change_description1')
        self.assertEqual(change_product.category.id, self.category2.id)
