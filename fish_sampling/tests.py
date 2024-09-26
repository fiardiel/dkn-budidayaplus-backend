from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from .models import Pond, FishSampling
from .api import router
import json
from rest_framework_simplejwt.tokens import AccessToken

class FishSamplingAPITest(TestCase):
    
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='userA', password='abc123')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_pond.png',
            volume=20000.0
        )
        self.fish_sampling = FishSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            fish_weight=1.5,
            fish_length=25.0,
            sample_date='2024-09-01'
        )
        self.fish_sampling_userA = FishSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            fish_weight=2.0,
            fish_length=50.0,
            sample_date='2024-09-10'
        )

    def test_add_fish_sampling(self):
        response = self.client.post('/', data=json.dumps({
            'pond_id': str(self.pond.pond_id),  
            'reporter_id': self.user.id,     
            'fish_weight': 2.0,
            'fish_length': 30.0,
            'sample_date': '2024-09-10'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)

    def test_get_fish_sampling(self):
        response = self.client.get(f'/{self.fish_sampling.sampling_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)

    def test_list_fish_samplings(self):
        response = self.client.get("/", headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        expected_data = [
                    {"id": str(self.fish_sampling.sampling_id), "reporter": self.fish_sampling.reporter.username},
                    {"id": str(self.fish_sampling_userA.sampling_id), "reporter": self.fish_sampling_userA.reporter.username},
                ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)

    def test_delete_fish_sampling(self):
        response = self.client.delete(f'/{self.fish_sampling.sampling_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_update_fish_sampling(self):
        response = self.client.put(f'/{self.fish_sampling.sampling_id}/', data=json.dumps({
            'pond_id': str(self.pond.pond_id),  
            'reporter_id': self.user.id,  
            'fish_weight': 2.5,
            'fish_length': 35.0,
            'sample_date': '2024-09-15'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)

    def test_add_fish_sampling_with_invalid_data(self):
        response = self.client.post('/', data=json.dumps({
            'sampling_id': str(self.fish_sampling.sampling_id),
            'pond_id': str(self.pond.pond_id),
            'reporter_id': self.user.id,
            'fish_weight': 1.2,
            'fish_length': -10.0,  # Invalid negative length
            'sample_date': '2024-09-19'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)  
    
    def test_update_fish_sampling_with_invalid_data(self):
        response = self.client.put(f'/{self.fish_sampling.sampling_id}/', data=json.dumps({
            'sampling_id': str(self.fish_sampling.sampling_id),
            'pond_id': str(self.pond.pond_id),
            'reporter_id': self.user.id,
            'fish_weight': -10.0,  # Invalid negative fish weight
            'fish_length': 4.5,
            'sample_date': '2024-09-19'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)  
    
    def test_list_fish_samplings_unauthorized(self):
        response = self.client.get('/', headers={})
        self.assertEqual(response.status_code, 401)