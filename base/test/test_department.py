import unittest
from unittest.mock import patch
from base import app


class DepartmentTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    def test_load_department_page(self, mock_login_session):
        response = self.app.get('/admin/load_department')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Department', response.data)  # Verify that the 'Add Department' page is loaded

    @patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    def test_insert_department(self, mock_login_session):
        response = self.app.post('/admin/insert_department', data=dict(
            departmentName="Computer Science",
            departmentDescription="CS Department",
            departmentDegreeId=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Department List', response.data)  # Verify successful insertion and redirection

    @patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    def test_view_departments(self, mock_login_session):
        response = self.app.get('/admin/view_department')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Department List', response.data)  # Verify that the 'View Departments' page is loaded

    @patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    def test_edit_department(self, mock_login_session):
        response = self.app.get('/admin/edit_department', query_string=dict(departmentId=1))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Department', response.data)  # Verify that the 'Edit Department' page is loaded

    @patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    def test_update_department(self, mock_login_session):
        response = self.app.post('/admin/update_department', data=dict(
            departmentId=1,
            departmentName="Updated Department Name",
            departmentDescription="Updated Description",
            departmentDegreeId=2
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Department List', response.data)  # Verify that the update succeeds and redirects

    @patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    def test_delete_department(self, mock_login_session):
        response = self.app.get('/admin/delete_department', query_string=dict(departmentId=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Department List', response.data)  # Verify successful deletion and redirection

    @patch('base.com.controller.login_controller.admin_login_session', return_value=None)
    def test_unauthorized_access(self, mock_login_session):
        response = self.app.get('/admin/load_department', follow_redirects=True)
        self.assertIn(b'Login', response.data)  # Verify redirection to the login page when unauthorized


if __name__ == '__main__':
    unittest.main()
