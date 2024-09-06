# Import necessary modules
import unittest
import sys
sys.path.insert(1, '../')
from App.auth.auth_salesforce import authSalesforce

#parameters: 
#description: test function for obtain tokens in salesforce
#return: result of the test
class TestAuthSalesforce(unittest.TestCase):
    #parameters: 
    #description: test function for obtain tokens in salesforce
    #return: result of the test
    def test_auth_salesforce_returns_valid_url(self):
        # Call the authSalesforce() function
        url = authSalesforce()

        # Verify that the URL is not empty and starts with "https://login.salesforce.com"
        self.assertTrue(url.startswith("https://login.salesforce.com"))
        self.assertNotEqual(url, "https://login.salesforce.com")  # Ensure it's not the home URL

if __name__ == '__main__':
    # Run the tests
    unittest.main()
