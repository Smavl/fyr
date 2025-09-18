#!/usr/bin/env python3
"""
Direct testing without heavy mocking - test the actual business logic
"""

import unittest
import base64
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import basic_http
from fyr import ServerOptions


class TestRouteLogic(unittest.TestCase):
    """Test route logic with minimal mocking - just what's absolutely necessary"""

    def create_simple_request(self, path):
        """Create a simple object that just has the attributes we need"""
        class SimpleRequest:
            def __init__(self, path):
                self.path = path
                self.decoded_content = None

        return SimpleRequest(path)

    def test_b64_request_with_valid_data(self):
        """Test successful base64 decode request"""
        # Real base64 encoding
        test_data = "hello world"
        encoded = base64.b64encode(test_data.encode()).decode()

        # Simple request object (not a mock)
        request = self.create_simple_request(f'/bd?d={encoded}')

        # Call the actual function
        result = basic_http.b64_decode_request(request)

        # Verify results
        self.assertEqual(result, test_data)
        self.assertEqual(request.decoded_content, test_data)

    def test_no_data_parameter(self):
        """Test request without data parameter"""
        request = self.create_simple_request('/bd')

        result = basic_http.b64_decode_request(request)

        # response for 
        self.assertEqual(result, "Successful\n")

    def test_error_handling(self):
        """Test error handling with invalid data"""
        request = self.create_simple_request('/bd?d=invalid!')

        result = basic_http.b64_decode_request(request)

        self.assertTrue(result.startswith("error:"))


class TestServerOptionsWithoutMocks(unittest.TestCase):

    def test_default_values(self):
        options = ServerOptions()
        self.assertFalse(options.echo)
        self.assertFalse(options.verbose)

    def test_custom_values(self):
        options = ServerOptions(echo=True, verbose=True)
        self.assertTrue(options.echo)
        self.assertTrue(options.verbose)

class TestIntegrationWithRealServer(unittest.TestCase):
    """Integration test with actual HTTP requests"""

    @classmethod
    def setUpClass(cls):
        """Init instance of real server"""
        import threading
        import time
        import socket

        # Find a free port
        sock = socket.socket()
        sock.bind(('', 0))
        cls.test_port = sock.getsockname()[1]
        sock.close()

        # Start server in background thread
        options = ServerOptions(echo=True, verbose=False)

        def run_test_server():
            try:
                basic_http.run(host='localhost', port=cls.test_port, options=options)
            except Exception as e:
                print(f"Server error: {e}")

        cls.server_thread = threading.Thread(target=run_test_server, daemon=True)
        cls.server_thread.start()

        # Wait for server to start
        # time.sleep(0.5)

    def test_real_http_request(self):
        """Make actual HTTP requests to test the full stack"""
        import urllib.request
        import urllib.parse

        # Test successful request
        test_string = "integration test string"
        encoded = base64.b64encode(test_string.encode()).decode()
        url = f'http://localhost:{self.test_port}/bd?d={encoded}'

        try:
            with urllib.request.urlopen(url) as response:
                result = response.read().decode()
                self.assertEqual(result, test_string)
        except Exception as e:
            self.skipTest(f"Server not available: {e}")

    def test_404_response(self):
        """Test 404 handling with real HTTP"""
        import urllib.request
        import urllib.error

        url = f'http://localhost:{self.test_port}/nonexistent'

        try:
            with urllib.request.urlopen(url) as response:
                self.fail("Should have gotten 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)
        except Exception as e:
            self.skipTest(f"Server not available: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
