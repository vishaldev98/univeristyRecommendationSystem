import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch, MagicMock
from base import app


# Fixture to set up Flask testing client
@pytest.fixture
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client


# Test for the admin login session check
@patch('base.com.controller.login_controller.admin_login_session')
def test_admin_login_session(mock_login_session, client):
    mock_login_session.return_value = "admin"

    # Test successful login session
    response = client.get('/admin/load_universitydetails')
    assert response.status_code == 200
    assert b"addUniversityDetails.html" in response.data  # Check if the correct page is loaded

    # Test invalid login session
    mock_login_session.return_value = "guest"
    response = client.get('/admin/load_universitydetails')
    assert response.status_code == 302  # Redirect to logout page
    assert response.location.endswith('/admin/logout')


# Test for loading university details page
@patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.view_universityinfo')
@patch('base.com.dao.degree_dao.DegreeDAO.view_degree')
@patch('base.com.controller.login_controller.admin_login_session')
def test_admin_load_universitydetails(mock_login_session, mock_view_universityinfo, mock_view_degree, client):
    mock_login_session.return_value = "admin"
    mock_view_universityinfo.return_value = [MagicMock(id=1, name="University 1")]
    mock_view_degree.return_value = [MagicMock(id=1, name="Degree 1")]

    response = client.get('/admin/load_universitydetails')
    assert response.status_code == 200
    assert b"addUniversityDetails.html" in response.data  # Check the page loads
    assert b"University 1" in response.data  # Check if university data is in the page
    assert b"Degree 1" in response.data  # Check if degree data is in the page


# Test for inserting university details
@patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.insert_universitydetails')
@patch('base.com.controller.login_controller.admin_login_session')
def test_admin_insert_universitydetails(mock_login_session, mock_insert_universitydetails, client):
    mock_login_session.return_value = "admin"

    form_data = {
        'universityDetailsUniversityInfoId': '1',
        'universityDetailsDegreeId': '1',
        'universityDetailsDepartmentId': '1',
        'universityDetailsCutOff': '75',
        'universityDetailsIelts': '6.5',
        'universityDetailsGre': '310'
    }

    response = client.post('/admin/insert_universitydetails', data=form_data)

    # Assert that the insert method is called once
    mock_insert_universitydetails.assert_called_once()

    # Check if the page redirects to view university details
    assert response.status_code == 302
    assert response.location == '/admin/view_universitydetails'


# Test for viewing university details
@patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.view_universitydetails')
@patch('base.com.controller.login_controller.admin_login_session')
def test_admin_view_universitydetails(mock_login_session, mock_view_universitydetails, client):
    mock_login_session.return_value = "admin"
    mock_view_universitydetails.return_value = [
        MagicMock(universitydetails_id=1, universitydetails_cutoff='70', universitydetails_ielts_score='6.5')
    ]

    response = client.get('/admin/view_universitydetails')

    assert response.status_code == 200
    assert b"viewUniversityDetails.html" in response.data  # Verify correct template is rendered
    assert b"70" in response.data  # Verify data appears in the response


# Test for deleting university details
@patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.delete_universitydetails')
@patch('base.com.controller.login_controller.admin_login_session')
def test_admin_delete_universitydetails(mock_login_session, mock_delete_universitydetails, client):
    mock_login_session.return_value = "admin"

    response = client.get('/admin/delete_universitydetails?universityDetailsId=1')

    # Assert the delete method is called
    mock_delete_universitydetails.assert_called_once()

    # Check the page redirects after deletion
    assert response.status_code == 302
    assert response.location == '/admin/view_universitydetails'


# Test for editing university details
@patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.edit_universitydetails')
@patch('base.com.dao.universityinfo_dao.UniversityInfoDAO.view_universityinfo')
@patch('base.com.dao.degree_dao.DegreeDAO.view_degree')
@patch('base.com.controller.login_controller.admin_login_session')
def test_admin_edit_universitydetails(mock_login_session, mock_view_universityinfo, mock_view_degree,
                                      mock_edit_universitydetails, client):
    mock_login_session.return_value = "admin"
    mock_view_universityinfo.return_value = [MagicMock(id=1, name="University 1")]
    mock_view_degree.return_value = [MagicMock(id=1, name="Degree 1")]
    mock_edit_universitydetails.return_value = [
        MagicMock(id=1, universitydetails_cutoff='70', universitydetails_ielts_score='6.5')]

    response = client.get('/admin/edit_universitydetails?universityDetailsId=1')

    assert response.status_code == 200
    assert b"editUniversityDetails.html" in response.data  # Check if the edit page is rendered
    assert b"University 1" in response.data  # Ensure the correct university info is present
    assert b"Degree 1" in response.data  # Ensure the degree list is loaded


# Test for updating university details
@patch('base.com.dao.universitydetails_dao.UniversityDetailsDAO.update_universitydetails')
@patch('base.com.controller.login_controller.admin_login_session')
def test_admin_update_universitydetails(mock_login_session, mock_update_universitydetails, client):
    mock_login_session.return_value = "admin"

    form_data = {
        'universityDetailsId': '1',
        'universityDetailsUniversityInfoId': '1',
        'universityDetailsDegreeId': '1',
        'universityDetailsDepartmentId': '1',
        'universityDetailsCutOff': '80',
        'universityDetailsIelts': '7.0',
        'universityDetailsGre': '320'
    }

    response = client.post('/admin/update_universitydetails', data=form_data)

    # Ensure the update method is called once
    mock_update_universitydetails.assert_called_once()

    # Check if the page redirects to view university details after update
    assert response.status_code == 302
    assert response.location == '/admin/view_universitydetails'


# Test for department details AJAX
@patch('base.com.dao.department_dao.DepartmentDAO.view_ajax_department_universitydetails')
@patch('base.com.controller.login_controller.admin_login_session')
def test_admin_ajax_department_universitydetails(mock_login_session, mock_view_ajax_department_universitydetails,
                                                 client):
    mock_login_session.return_value = "admin"

    # Mock response for department data
    mock_view_ajax_department_universitydetails.return_value = [
        MagicMock(department_id=1, department_name="Computer Science")
    ]

    # Simulate the AJAX GET request
    response = client.get('/admin/ajax_department_universitydetails?universityDetailsDegreeId=1')

    assert response.status_code == 200
    assert b'Computer Science' in response.data  # Ensure department data is returned
