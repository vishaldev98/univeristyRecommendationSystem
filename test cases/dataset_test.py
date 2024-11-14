import os
import pytest
from datetime import datetime
from unittest import mock
from base import app
from werkzeug.datastructures import FileStorage
from base.com.controller.login_controller import admin_login_session
from base.com.dao.dataset_dao import DatasetDAO
from base.com.vo.dataset_vo import DatasetVO


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Test for admin_load_dataset route
def test_admin_load_dataset(client, mocker):
    # Mock admin login session
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")

    response = client.get('/admin/load_dataset')
    assert response.status_code == 200
    assert b'Add Dataset' in response.data  # Verify that 'Add Dataset' page is rendered


# Test for admin_insert_dataset route
def test_admin_insert_dataset(client, mocker):
    # Mock admin login session
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")

    # Mock file storage and dataset DAO
    mock_file = mock.MagicMock(spec=FileStorage)
    mock_file.filename = "test_dataset.csv"
    mock_file.save = mock.MagicMock()

    mocker.patch('werkzeug.utils.secure_filename', return_value="test_dataset.csv")
    mocker.patch('os.path.join', return_value='base/static/adminResources/dataset/test_dataset.csv')

    data = {
        'datasetFile': mock_file,
        'datasetDescription': 'Test dataset description'
    }

    # Mock insert_dataset method in DatasetDAO
    mock_dao = mocker.patch('base.com.dao.dataset_dao.DatasetDAO.insert_dataset')

    response = client.post('/admin/insert_dataset', data=data, follow_redirects=True)
    assert response.status_code == 200
    mock_file.save.assert_called_once()
    mock_dao.assert_called_once()


# Test for admin_view_dataset route
def test_admin_view_dataset(client, mocker):
    # Mock admin login session
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")

    # Mock DatasetDAO and its method
    mock_dao = mocker.patch('base.com.dao.dataset_dao.DatasetDAO.view_dataset')
    mock_dao.return_value = [DatasetVO(dataset_file_name="test_dataset.csv", dataset_description="Test description")]

    response = client.get('/admin/view_dataset')
    assert response.status_code == 200
    assert b'View Dataset' in response.data  # Verify that 'View Dataset' page is rendered


# Test for admin_delete_dataset route
def test_admin_delete_dataset(client, mocker):
    # Mock admin login session
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")

    # Mock DatasetDAO delete method and dataset file path
    mock_dao = mocker.patch('base.com.dao.dataset_dao.DatasetDAO.delete_dataset')
    mock_dao.return_value = DatasetVO(dataset_file_path="..", dataset_file_name="test_dataset.csv")

    # Mock os.remove to prevent actual file deletion during the test
    mock_remove = mocker.patch('os.remove')

    response = client.get('/admin/delete_dataset', query_string={'datasetId': '1'}, follow_redirects=True)
    assert response.status_code == 200
    mock_remove.assert_called_once_with('base/static/adminResources/dataset/test_dataset.csv')
    mock_dao.assert_called_once_with('1')
