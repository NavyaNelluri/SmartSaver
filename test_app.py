import unittest
from app import app, get_db, send_email
from unittest.mock import patch
import unittest.mock
from unittest.mock import patch, Mock
from app import send_expense_notification  



class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_db')
    def test_register_success(self, mock_get_db):
        mock_cursor = unittest.mock.Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor

        # Simulate that there are no existing users with the given username
        mock_cursor.fetchone.side_effect = [None, None]

        # Perform the POST request to register a new user
        response = self.app.post('/register', data={
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'password': 'password123',
            'email': 'john@example.com'
        }, follow_redirects=True)  # Follow the redirect to check the final response

        # Check the final response after redirect
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)
        mock_cursor.execute.assert_called()

    @patch('app.get_db')
    @patch('app.send_email')
    def test_register_existing_username(self, mock_send_email, mock_get_db):
        mock_cursor = unittest.mock.Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor

        # Simulate that the username already exists
        mock_cursor.fetchone.side_effect = [(1,), None]

        response = self.app.post('/register', data={
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'password': 'password123',
            'email': 'john@example.com'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists', response.data)

    @patch('app.get_db')
    def test_login_success(self, mock_get_db):
        mock_cursor = unittest.mock.Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor

        # Simulate a successful login
        mock_cursor.fetchone.return_value = ('John', 'Doe', 'johndoe', 'password123', 'john@example.com')

        response = self.app.post('/', data={
            'username': 'johndoe',
            'password': 'password123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, johndoe', response.data)  # Check if welcome message is present


    @patch('app.get_db')
    def test_forgot_password_success(self, mock_get_db):
        mock_cursor = unittest.mock.Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor

        # Simulate that the user exists for password reset
        mock_cursor.fetchone.return_value = ('John', 'Doe', 'johndoe', 'oldpassword', 'john@example.com')

        response = self.app.post('/forgot_password', data={
            'username': 'johndoe',
            'email': 'john@example.com',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password has been reset successfully', response.data)  # Check if welcome message is present


    @patch('app.get_db')
    def test_delete_goal_success(self, mock_get_db):
        mock_cursor = unittest.mock.Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor

        response = self.app.post('/delete_goal', data={
            'created_at': '2024-01-01T00:00:00'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    @patch('app.get_db')
    def test_view_income(self, mock_get_db):
        mock_cursor = unittest.mock.Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor

        # Simulate returning income records
        mock_cursor.fetchall.return_value = [
            ('Job', 'Monthly', 5000, 1),
            ('Freelance', 'One-time', 1500, 2)
        ]

        with self.app.session_transaction() as sess:
            sess['username'] = 'johndoe'

        response = self.app.get('/view_income')

        self.assertEqual(response.status_code, 200)
    @patch('app.get_db')
    def test_forgot_password_failure(self, mock_get_db):
        mock_cursor = unittest.mock.Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor
    
        # Simulate that the user exists but the new passwords do not match
        mock_cursor.fetchone.return_value = ('John', 'Doe', 'johndoe', 'oldpassword', 'john@example.com')
    
        response = self.app.post('/forgot_password', data={
            'username': 'johndoe',
            'email': 'john@example.com',
            'new_password': 'newpassword123',
            'confirm_password': 'differentpassword123'
        }, follow_redirects=True)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords do not match', response.data)
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.mock_session = {}  # Create a mock session dictionary

    def tearDown(self):
        pass

    @patch('app.get_db')
    @patch('app.send_expense_notification')
    def test_add_expense_success(self, mock_send_expense_notification, mock_get_db):
        # Mock database cursor and fetch user info
        mock_cursor = Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('John Doe', 'johndoe@example.com')

        # Simulate login by setting mock session data
        self.mock_session['username'] = 'johndoe'
        with self.app.session_transaction() as session:
            session.update(self.mock_session)

        # Send POST request to add an expense
        response = self.app.post('/dashboard', data={
            'form_type': 'expense',
            'expense_type': 'Utilities',
            'frequency': 'Monthly',
            'Notes': 'Electricity',
            'dollars': '100'
        }, follow_redirects=True)

        # Check response and if notification was sent
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_send_expense_notification.called)
    @patch('app.get_db')
    @patch('app.send_income_notification')  # Replace with the correct function if different
    def test_add_income_success(self, mock_send_income_notification, mock_get_db):
        # Mock database cursor and fetch user info
        mock_cursor = Mock()
        mock_get_db.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('John Doe', 'johndoe@example.com')

        # Simulate login by setting mock session data
        self.mock_session['username'] = 'johndoe'
        with self.app.session_transaction() as session:
            session.update(self.mock_session)

        # Send POST request to add an income
        response = self.app.post('/dashboard', data={
            'form_type': 'income',
            'frequency': 'Monthly',
            'Notes': 'Salary',
            'dollars': '5000'
        }, follow_redirects=True)

        # Check response and if notification was sent
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_send_income_notification.called)
if __name__ == '__main__':
    unittest.main()
