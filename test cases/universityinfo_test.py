import pytest
from flask import url_for
from base import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_admin_load_universityinfo(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    response = client.get('/admin/load_universityinfo')
    assert response.status_code == 200
    assert b'Add University Info' in response.data  # Check for page content (modify as needed)

def test_admin_insert_universityinfo(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_insert = mocker.patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.insert_universityinfo')

    data = {
        'universityInfoName': 'Test University',
        'universityInfoAddress': '123 Test St',
        'universityInfoFees': '5000',
        'universityInfoContact': '1234567890',
        'universityInfoEmail': 'test@university.com',
        'universityInfoDescription': 'Test description'
    }
    response = client.post('/admin/insert_universityinfo', data=data)
    assert response.status_code == 302  # Should redirect after insertion
    mock_insert.assert_called_once()  # Verify that insertion was attempted

def test_admin_view_universityinfo(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_view = mocker.patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.view_universityinfo')
    mock_view.return_value = []

    response = client.get('/admin/view_universityinfo')
    assert response.status_code == 200
    assert b'University Info' in response.data  # Check for content (modify as needed)

def test_admin_delete_universityinfo(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_delete = mocker.patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.delete_universityinfo')

    response = client.get('/admin/delete_universityinfo?universityInfoId=1')
    assert response.status_code == 302  # Should redirect after deletion
    mock_delete.assert_called_once()  # Verify that deletion was attempted

def test_admin_edit_universityinfo(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_edit = mocker.patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.edit_universityinfo')
    mock_edit.return_value = []

    response = client.get('/admin/edit_universityinfo?universityInfoId=1')
    assert response.status_code == 200
    assert b'Edit University Info' in response.data  # Check for content (modify as needed)

def test_admin_update_universityinfo(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_update = mocker.patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.update_universityinfo')

    data = {
        'universityInfoId': '1',
        'universityInfoName': 'Updated University',
        'universityInfoAddress': '123 Updated St',
        'universityInfoFees': '6000',
        'universityInfoContact': '0987654321',
        'universityInfoEmail': 'updated@university.com',
        'universityInfoDescription': 'Updated description'
    }
    response = client.post('/admin/update_universityinfo', data=data)
    assert response.status_code == 302  # Should redirect after update
    mock_update.assert_called_once()  # Verify that update was attempted
