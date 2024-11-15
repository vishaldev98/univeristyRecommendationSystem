import unittest
from base import app
from flask import Flask


class TestCountryRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test client for all tests."""
        app.testing = True  # Enable testing mode
        cls.client = app.test_client()  # Set up Flask test client

    def test_admin_load_country(self):
        """Test the load country page route."""
        response = self.client.get('/admin/load_country')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Country', response.data)  # Check if "Add Country" appears in the HTML

    def test_admin_insert_country(self):
        """Test the insertion of a new country."""
        data = {
            'countryName': 'TestCountry',
            'countryDescription': 'TestDescription'
        }
        response = self.client.post('/admin/insert_country', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestCountry', response.data)  # Check if the country is inserted successfully

    def test_admin_view_country(self):
        response = self.client.get('/admin/view_country')

        # Debug print for response data
        print(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)  # Ensure the response status is OK
        self.assertIn(b'Country List', response.data)  # Check if the country list page is loaded

    def test_admin_delete_country(self):
        """Test deletion of a country."""
        # Add a country first for testing delete functionality
        data = {
            'countryName': 'DeleteCountry',
            'countryDescription': 'ToBeDeleted'
        }
        self.client.post('/admin/insert_country', data=data)

        # Assuming the countryId is fetched dynamically after insertion
        response = self.client.get('/admin/view_country')
        country_id = extract_country_id(response.data, 'DeleteCountry')  # Helper function to extract ID

        delete_response = self.client.get(f'/admin/delete_country?countryId={country_id}', follow_redirects=True)
        self.assertEqual(delete_response.status_code, 200)
        self.assertNotIn(b'DeleteCountry', delete_response.data)  # Check if the country is removed successfully

    def test_admin_edit_country(self):
        """Test editing a country."""
        # Add a country first for testing the edit functionality
        data = {
            'countryName': 'EditCountry',
            'countryDescription': 'EditableDescription'
        }
        self.client.post('/admin/insert_country', data=data)

        response = self.client.get('/admin/view_country')
        country_id = extract_country_id(response.data, 'EditCountry')  # Extract ID

        # Edit the country
        edit_data = {
            'countryId': country_id,
            'countryName': 'UpdatedCountry',
            'countryDescription': 'UpdatedDescription'
        }
        update_response = self.client.post('/admin/update_country', data=edit_data, follow_redirects=True)
        self.assertEqual(update_response.status_code, 200)
        self.assertIn(b'UpdatedCountry', update_response.data)  # Check if the country was updated successfully


def extract_country_id(html_data, country_name):
    """Helper function to extract the countryId for a specific country."""
    # Implement this function based on your HTML structure
    # You could use regex or BeautifulSoup to extract the countryId from the response
    pass


if __name__ == '__main__':
    unittest.main()