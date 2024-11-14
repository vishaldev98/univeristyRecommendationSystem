import pytest
from flask import url_for
from base import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_admin_load_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_universityinfo = mocker.patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.view_universityinfo')
    mock_degree = mocker.patch('base.com.dao.degree_dao.DegreeDAO.view_degree')

    mock_universityinfo.return_value = []
    mock_degree.return_value = []

    response = client.get('/admin/load_universitydetails')
    assert response.status_code == 200
    assert b'Add University Details' in response.data  # Modify this to match expected page content

def test_admin_ajax_department_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_department_dao = mocker.patch('base.com.dao.department_dao.DepartmentDAO.view_ajax_department_universitydetails')
    mock_department_dao.return_value = []

    response = client.get('/admin/ajax_department_universitydetails?universityDetailsDegreeId=1')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []  # Expect empty JSON due to mocked return

def test_admin_insert_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_insert = mocker.patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.insert_universitydetails')

    data = {
        'universityDetailsUniversityInfoId': '1',
        'universityDetailsDegreeId': '1',
        'universityDetailsDepartmentId': '1',
        'universityDetailsCutOff': '85',
        'universityDetailsIelts': '6.5',
        'universityDetailsGre': '320'
    }
    response = client.post('/admin/insert_universitydetails', data=data)
    assert response.status_code == 302  # Redirect after successful insert
    mock_insert.assert_called_once()  # Verify insertion

def test_admin_view_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_view = mocker.patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.view_universitydetails')
    mock_view.return_value = []

    response = client.get('/admin/view_universitydetails')
    assert response.status_code == 200
    assert b'University Details' in response.data  # Modify to match expected page content

def test_admin_delete_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_delete = mocker.patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.delete_universitydetails')

    response = client.get('/admin/delete_universitydetails?universityDetailsId=1')
    assert response.status_code == 302  # Redirect after deletion
    mock_delete.assert_called_once()  # Verify delete

def test_admin_edit_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_edit = mocker.patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.edit_universitydetails')
    mock_universityinfo = mocker.patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.view_universityinfo')
    mock_degree = mocker.patch('base.com.dao.degree_dao.DegreeDAO.view_degree')

    mock_edit.return_value = []
    mock_universityinfo.return_value = []
    mock_degree.return_value = []

    response = client.get('/admin/edit_universitydetails?universityDetailsId=1')
    assert response.status_code == 200
    assert b'Edit University Details' in response.data  # Modify to match expected content

def test_admin_update_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_update = mocker.patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.update_universitydetails')

    data = {
        'universityDetailsId': '1',
        'universityDetailsUniversityInfoId': '1',
        'universityDetailsDegreeId': '1',
        'universityDetailsDepartmentId': '1',
        'universityDetailsCutOff': '90',
        'universityDetailsIelts': '7.0',
        'universityDetailsGre': '330'
    }
    response = client.post('/admin/update_universitydetails', data=data)
    assert response.status_code == 302  # Redirect after update
    mock_update.assert_called_once()  # Verify update
