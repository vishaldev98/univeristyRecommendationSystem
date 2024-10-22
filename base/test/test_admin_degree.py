import unittest
from flask import Flask
from base import app


class AdminDegreeTestCase(unittest.TestCase):
    def setUp(self):
        # Setup Flask test client
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        # Clean up any resources if necessary
        pass

    def test_admin_load_degree(self):
        with self.client:
            response = self.client.get('/admin/load_degree')
            self.assertEqual(response.status_code, 302)  # Redirect due to lack of admin login

    def test_admin_insert_degree(self):
        with self.client:
            response = self.client.post('/admin/insert_degree', data={
                'degreeName': 'Test Degree',
                'degreeDescription': 'Test Description'
            })
            self.assertEqual(response.status_code, 302)
    def test_admin_view_degree(self):
        with self.client:
            response = self.client.get('/admin/view_degree')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'viewDegree.html', response.data)
    def test_admin_delete_degree(self):
        with self.client:
            response = self.client.get('/admin/delete_degree?degreeId=1')
            self.assertEqual(response.status_code, 302)
    def test_admin_edit_degree(self):
        with self.client:
            response = self.client.get('/admin/edit_degree?degreeId=1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'editDegree.html', response.data)
    def test_admin_update_degree(self):
        with self.client:
            response = self.client.post('/admin/update_degree', data={
                'degreeId': '1',
                'degreeName': 'Updated Degree',
                'degreeDescription': 'Updated Description'
            })
            self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
