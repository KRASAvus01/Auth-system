from rest_framework.test import APIClient, APITestCase


class ArticleAccessTests(APITestCase):
    def test_unauthorized_access(self):
        client = APIClient()
        response = client.get("/api/products/")
        self.assertEqual(response.status_code, 401)