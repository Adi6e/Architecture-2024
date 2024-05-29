import unittest
import requests

BASE_URL = "http://127.0.0.1:8080"
order_id: str = ""


class TestAPI(unittest.TestCase):
    def setUp(self):
        order_data = {
            "name": "Test order",
            "description": "testing...bla.bla.bla",
            "services": []
        }
        response = requests.post(
            f"{BASE_URL}/orders/", json=order_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.text)
        self.order_id = response.json()

    def test_create_order(self):
        pass  # Nothing to do, order already created in setUp() method

    def test_read_order(self):
        response = requests.get(f"{BASE_URL}/orders/{self.order_id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    def test_update_order(self):
        updated_order_data = {
            "name": "Updated order",
            "description": "updated description...",
            "reports": []
        }
        response = requests.put(
            f"{BASE_URL}/orders/{self.order_id}", json=updated_order_data)
        self.assertEqual(response.status_code, 200)
        # Expecting 1, as one document was updated
        self.assertEqual(response.json(), 1)

    def test_delete_order(self):
        response = requests.delete(
            f"{BASE_URL}/orders/{self.order_id}")
        self.assertEqual(response.status_code, 200)
        # Expecting 1, as one document was deleted
        self.assertEqual(response.json(), 1)


if __name__ == '__main__':
    unittest.main()
