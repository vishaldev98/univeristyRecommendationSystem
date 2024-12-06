import os
import pytest
from flask import Flask, request
from flask_testing import TestCase
from unittest import mock
from base import app
from base.com.dao.dataset_dao import DatasetDAO
from base.com.vo.dataset_vo import DatasetVO
from werkzeug.utils import secure_filename


class TestDatasetApp(TestCase):

    def create_app(self):
        # Setting up the app for testing
        app.config['TESTING'] = True
        app.config['DATASET_FOLDER'] = 'base/static/adminResources/dataset/'
        return app

    @mock.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    def test_admin_load_dataset(self, mock_login):
        """Test admin_load_dataset route"""
        response = self.client.get('/admin/load_dataset')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/addDataset.html')

    @mock.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    @mock.patch('werkzeug.utils.secure_filename', return_value="test_dataset.csv")
    @mock.patch('flask.request.files.get', return_value=mock.Mock(filename="test_dataset.csv"))
    @mock.patch('os.path.join', return_value="base/static/adminResources/dataset/test_dataset.csv")
    @mock.patch('flask.request.form.get', return_value="Test dataset description")
    @mock.patch('base.com.dao.dataset_dao.DatasetDAO.insert_dataset', return_value=None)
    def test_admin_insert_dataset(self, mock_insert_dataset, mock_form, mock_get_file, mock_secure_filename, mock_os_path):
        """Test admin_insert_dataset route"""
        data = {
            'datasetFile': (mock.Mock(), 'test_dataset.csv'),
            'datasetDescription': 'Test dataset description'
        }
        response = self.client.post('/admin/insert_dataset', data=data, follow_redirects=True)
        self.assertRedirects(response, '/admin/view_dataset')
        mock_insert_dataset.assert_called_once()

    @mock.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    @mock.patch('base.com.dao.dataset_dao.DatasetDAO.view_dataset', return_value=[{
        'dataset_id': 1,
        'dataset_file_name': 'test_dataset.csv',
        'dataset_description': 'Test dataset description'
    }])
    def test_admin_view_dataset(self, mock_view_dataset, mock_login):
        """Test admin_view_dataset route"""
        response = self.client.get('/admin/view_dataset')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/viewDataset.html')
        self.assertIn(b'test_dataset.csv', response.data)
        self.assertIn(b'Test dataset description', response.data)

    @mock.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    @mock.patch('base.com.dao.dataset_dao.DatasetDAO.delete_dataset', return_value=DatasetVO(dataset_file_path="base/static/adminResources/dataset/", dataset_file_name="test_dataset.csv"))
    @mock.patch('os.remove', return_value=None)
    def test_admin_delete_dataset(self, mock_remove, mock_delete_dataset, mock_login):
        """Test admin_delete_dataset route"""
        response = self.client.get('/admin/delete_dataset?datasetId=1')
        self.assertRedirects(response, '/admin/view_dataset')
        mock_delete_dataset.assert_called_once()
        mock_remove.assert_called_once()

    @mock.patch('base.com.controller.login_controller.admin_login_session', return_value="invalid_admin")
    def test_admin_load_dataset_invalid_session(self, mock_login):
        """Test admin_load_dataset route with invalid session"""
        response = self.client.get('/admin/load_dataset')
        self.assertRedirects(response, '/admin/logout')

    @mock.patch('base.com.controller.login_controller.admin_login_session', return_value="invalid_admin")
    def test_admin_insert_dataset_invalid_session(self, mock_login):
        """Test admin_insert_dataset route with invalid session"""
        data = {
            'datasetFile': (mock.Mock(), 'test_dataset.csv'),
            'datasetDescription': 'Test dataset description'
        }
        response = self.client.post('/admin/insert_dataset', data=data)
        self.assertRedirects(response, '/admin/logout')

    @mock.patch('base.com.controller.login_controller.admin_login_session', return_value="invalid_admin")
    def test_admin_view_dataset_invalid_session(self, mock_login):
        """Test admin_view_dataset route with invalid session"""
        response = self.client.get('/admin/view_dataset')
        self.assertRedirects(response, '/admin/logout')

    @mock.patch('base.com.controller.login_controller.admin_login_session', return_value="invalid_admin")
    def test_admin_delete_dataset_invalid_session(self, mock_login):
        """Test admin_delete_dataset route with invalid session"""
        response = self.client.get('/admin/delete_dataset?datasetId=1')
        self.assertRedirects(response, '/admin/logout')


if __name__ == "__main__":
    pytest.main()
