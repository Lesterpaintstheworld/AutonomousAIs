import unittest
from api import app, patterns, users

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_patterns(self):
        response = self.app.get('/api/patterns')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_pattern(self):
        new_pattern = {
            "name": "Test Pattern",
            "content": "C4 D4 E4 F4",
            "user_id": "1"
        }
        response = self.app.post('/api/patterns', json=new_pattern)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_get_specific_pattern(self):
        # Assuming there's at least one pattern in the database
        response = self.app.get('/api/patterns/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.json)
        self.assertIn("content", response.json)

    def test_update_pattern(self):
        updated_pattern = {
            "name": "Updated Test Pattern",
            "content": "G4 A4 B4 C5"
        }
        response = self.app.put('/api/patterns/1', json=updated_pattern)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Test Pattern")

    def test_delete_pattern(self):
        response = self.app.delete('/api/patterns/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Pattern deleted successfully")

if __name__ == '__main__':
    unittest.main()
