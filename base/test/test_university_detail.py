import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest import mock
from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.universitydetails_dao import UniversityDetailsDAO
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.department_dao import DepartmentDAO
from base.com.dao.universityinfo_dao import UniversityInfoDAO


@pytest.fixture
def client() -> FlaskClient:
    """Fixture for setting up a Flask test client."""
    app.config['TESTING'] = True
    return app.test_client()


# 1. Test Case: admin_load_universitydetails
def test_admin_load_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_universityinfo_dao = mocker.patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.view_universityinfo',
                                           return_value=[...])
    mock_degree_dao = mocker.patch('base.com.dao.degree_dao.DegreeDAO.view_degree', return_value=[...])
    response = client.get('/admin/load_universitydetails')
    assert response.status_code == 200
    assert b'addUniversityDetails.html' in response.data
    assert mock_universityinfo_dao.called
    assert mock_degree_dao.called


# 2. Test Case: admin_ajax_department_universitydetails
def test_admin_ajax_department_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_department_dao = mocker.patch(
        'base.com.dao.department_dao.DepartmentDAO.view_ajax_department_universitydetails', return_value=[...])

    # Send GET request
    response = client.get('/admin/ajax_department_universitydetails?universityDetailsDegreeId=1')

    # Assertions
    assert response.status_code == 200
    assert response.is_json
    assert mock_department_dao.called
    assert b'ajax_universityDetails_department' in response.data


# 3. Test Case: admin_insert_universitydetails
def test_admin_insert_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_universitydetails_dao = mocker.patch(
        'base.com.dao.universitydetails_dao.UniversityDetailsDAO.insert_universitydetails')
    form_data = {
        'universityDetailsUniversityInfoId': 1,
        'universityDetailsDegreeId': 2,
        'universityDetailsDepartmentId': 3,
        'universityDetailsCutOff': '80',
        'universityDetailsIelts': '6.5',
        'universityDetailsGre': '300'
    }
    response = client.post('/admin/insert_universitydetails', data=form_data)
    assert response.status_code == 302  # Redirect status code
    assert response.location == '/admin/view_universitydetails'
    assert mock_universitydetails_dao.called


# 4. Test Case: admin_view_universitydetails
def test_admin_view_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_universitydetails_dao = mocker.patch(
        'base.com.dao.universitydetails_dao.UniversityDetailsDAO.view_universitydetails', return_value=[...])
    response = client.get('/admin/view_universitydetails')
    assert response.status_code == 200
    assert b'viewUniversityDetails.html' in response.data
    assert mock_universitydetails_dao.called


# 5. Test Case: admin_delete_universitydetails
def test_admin_delete_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_universitydetails_dao = mocker.patch(
        'base.com.dao.universitydetails_dao.UniversityDetailsDAO.delete_universitydetails')
    response = client.get('/admin/delete_universitydetails?universityDetailsId=1')
    assert response.status_code == 302  # Redirect status code
    assert response.location == '/admin/view_universitydetails'
    assert mock_universitydetails_dao.called


# 6. Test Case: admin_edit_universitydetails
def test_admin_edit_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_universitydetails_dao = mocker.patch(
        'base.com.dao.universitydetails_dao.UniversityDetailsDAO.edit_universitydetails', return_value=[...])
    response = client.get('/admin/edit_universitydetails?universityDetailsId=1')
    assert response.status_code == 200
    assert b'editUniversityDetails.html' in response.data
    assert mock_universitydetails_dao.called


# 7. Test Case: admin_update_universitydetails
def test_admin_update_universitydetails(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="admin")
    mock_universitydetails_dao = mocker.patch(
        'base.com.dao.universitydetails_dao.UniversityDetailsDAO.update_universitydetails')
    form_data = {
        'universityDetailsId': 1,
        'universityDetailsUniversityInfoId': 2,
        'universityDetailsDegreeId': 3,
        'universityDetailsDepartmentId': 4,
        'universityDetailsCutOff': '85',
        'universityDetailsIelts': '7.0',
        'universityDetailsGre': '320'
    }
    response = client.post('/admin/update_universitydetails', data=form_data)
    assert response.status_code == 302  # Redirect status code
    assert response.location == '/admin/view_universitydetails'
    assert mock_universitydetails_dao.called
