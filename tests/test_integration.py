import unittest
from app import create_app
from database import db

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_get_pattern(self):
        # Create a new pattern
        response = self.client.post('/api/patterns', json={
            'name': 'Test Pattern',
            'instrument': 'drums',
            'pattern': [1, 0, 1, 0, 1, 0, 1, 0]
        })
        self.assertEqual(response.status_code, 201)
        pattern_id = response.json['id']

        # Get the created pattern
        response = self.client.get(f'/api/patterns/{pattern_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Pattern')
        self.assertEqual(response.json['instrument'], 'drums')
        self.assertEqual(response.json['pattern'], [1, 0, 1, 0, 1, 0, 1, 0])

    def test_update_and_delete_pattern(self):
        # Create a new pattern
        response = self.client.post('/api/patterns', json={
            'name': 'Original Pattern',
            'instrument': 'synth',
            'pattern': [1, 1, 1, 1]
        })
        self.assertEqual(response.status_code, 201)
        pattern_id = response.json['id']

        # Update the pattern
        response = self.client.put(f'/api/patterns/{pattern_id}', json={
            'name': 'Updated Pattern',
            'instrument': 'synth',
            'pattern': [0, 1, 0, 1]
        })
        self.assertEqual(response.status_code, 200)

        # Verify the update
        response = self.client.get(f'/api/patterns/{pattern_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Pattern')
        self.assertEqual(response.json['pattern'], [0, 1, 0, 1])

        # Delete the pattern
        response = self.client.delete(f'/api/patterns/{pattern_id}')
        self.assertEqual(response.status_code, 204)

        # Verify the deletion
        response = self.client.get(f'/api/patterns/{pattern_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
