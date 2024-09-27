from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .views import PostListCreateView

User = get_user_model()


class HeloWorldTestCase(APITestCase):
    def test_hellow_world(self):
        response = self.client.get(reverse("posts_home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Hello, World!")


class PostListCreateTestCase(APITestCase):
    # def setup(self):
    #     self.factory = APIRequestFactory()
    #     self.view = PostListCreateView.as_view()
    #     self.url = reverse("list_posts")
    #     self.user = User.objects.create(
    #         username="nandom", email="nandom@nandom.com", password="Blessedacademy"
    #     )
    def authenticate(self):
        self.client.post(
            reverse("signup"),
            {
                "username": "nandom",
                "email": "nandom@nandom.com",
                "password": "Blessedacademy",
            },
        )
        response = self.client.post(
            reverse("login"),
            {
                "email": "nandom@nandom.com",
                "password": "Blessedacademy",
            },
        )

        token = response.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_posts(self):
        # self.factory = APIRequestFactory()
        # self.view = PostListCreateView.as_view()
        self.url = reverse("list_posts")
        # request = self.factory.get(self.url)
        # response = self.view(request)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])

    def test_post_creation(self):
        # self.factory = APIRequestFactory()
        # self.view = PostListCreateView.as_view()
        # self.url = reverse("list_posts")
        # self.user = User.objects.create(
        #     username="nandom", email="nandom@nandom.com", password="Blessedacademy"
        # )
        sample_post = {"title": "sample title", "content": "sample content"}
        # request = self.factory.post(self.url, sample_post)
        # request.user = self.user
        # response = self.view(request)

        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.authenticate()
        response = self.client.post(reverse("list_posts"), sample_post)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "sample title")
