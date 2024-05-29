import unittest
import requests

BASE_URL = "http://127.0.0.1:8081"
service_id: str = ""


class TestAPI(unittest.TestCase):
    def setUp(self):
        service_data = {
            "title": "Test Service",
            "description": "Test Description",
            "creator_id": 5
        }
        response = requests.post(f"{BASE_URL}/services/", json=service_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("service_id", response.json())
        self.service_id = response.json()['service_id']

    def test_create_service(self):
        pass

    def test_read_service(self):
        response = requests.get(f"{BASE_URL}/services/{self.service_id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    def test_update_service(self):
        updated_service_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "creator_id": 6
        }
        response = requests.put(
            f"{BASE_URL}/services/{self.service_id}", json=updated_service_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Услуга успешно обновлена.")

    def test_delete_service(self):
        response = requests.delete(f"{BASE_URL}/services/{self.service_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Услуга успешно удалена.")


if __name__ == '__main__':
    unittest.main()
