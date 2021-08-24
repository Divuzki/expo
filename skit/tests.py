from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Skit
User = get_user_model()

class SkitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='divine', password='somepassword')
        self.userb = User.objects.create_user(username='divine-2', password='somepassword2')
        Skit.objects.create(content="my first skit", 
            user=self.user)
        Skit.objects.create(content="my first skit", 
            user=self.user)
        Skit.objects.create(content="my first skit", 
            user=self.userb)
        self.currentCount = Skit.objects.all().count()

    def test_skit_created(self):
        skit_obj = Skit.objects.create(content="my second skit", 
            user=self.user)
        self.assertEqual(skit_obj.id, 4)
        self.assertEqual(skit_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client
    
    def test_skit_list(self):
        client = self.get_client()
        response = client.get("/api/skits/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_skit_list(self):
        client = self.get_client()
        response = client.get("/api/skits/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
    def test_skit_related_name(self):
        user = self.user
        self.assertEqual(user.skit.count(), 2)
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/skits/action/", 
            {"id": 1, "action": "like"})
        like_count = response.json().get("likes")
        user = self.user
        my_like_instances_count = user.skitlike_set.count()
        my_retated_likes = user.skit_user.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        self.assertEqual(my_like_instances_count, 1)
        self.assertEqual(my_retated_likes, 1)
    
    def test_action_dislike(self):
        client = self.get_client()
        response = client.post("/api/skits/action/", 
            {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/skits/action/", 
            {"id": 2, "action": "dislike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_action_repost(self):
        client = self.get_client()
        response = client.post("/api/skits/action/", 
            {"id": 2, "action": "repost"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_skit_id = data.get("id")
        self.assertNotEqual(2, new_skit_id)
        self.assertEqual(self.currentCount + 1, new_skit_id)

    def test_skit_create_api_view(self):
        request_data = {"content": "This is my test skit"}
        client = self.get_client()
        response = client.post("/api/skits/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_skit_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_skit_id)
    
    def test_skit_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/skits/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_skit_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/skits/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/skits/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/skits/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)