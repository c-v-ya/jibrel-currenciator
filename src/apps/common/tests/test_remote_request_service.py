from unittest.mock import patch, Mock

from django.test import TestCase

from src.apps.common.enums import RequestMethod
from src.apps.common.services import RemoteRequest


class RemoteRequestModelTest(TestCase):
    test_url = 'http://test.url'
    test_headers = {'Content-type': 'application/json'}

    @patch('src.apps.common.services.remote_request.requests.get')
    def test_send_GET_request(self, mock_requests_get):
        r_request = RemoteRequest(
            url=self.test_url,
            method=RequestMethod.GET,
            basic_auth=None,
            headers=self.test_headers,
            request_data=None
        )
        mock_requests_get.return_value.ok = True
        response = r_request.send_request()
        self.assertTrue(response.ok)

    @patch('src.apps.common.services.remote_request.requests.post')
    def test_send_POST_json_request(self, mock_requests_post):
        r_request = RemoteRequest(
            url=self.test_url,
            method=RequestMethod.POST,
            headers=self.test_headers,
            basic_auth=None,
            request_data=None
        )
        mock_requests_post.return_value.ok = True
        response = r_request.send_request()
        self.assertTrue(response.ok)

    @patch('src.apps.common.services.remote_request.requests.post')
    def test_send_POST_data_request(self, mock_requests_post):
        headers = self.test_headers.copy()
        headers['Content-type'] = 'plain/text'
        r_request = RemoteRequest(
            url=self.test_url,
            method=RequestMethod.POST,
            headers=headers,
            basic_auth=None,
            request_data=None
        )
        mock_requests_post.return_value.ok = True
        response = r_request.send_request()
        self.assertTrue(response.ok)

    def test_collect_response_json_data(self):
        mock_response = Mock()
        mock_data = {'test': 'test'}
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        data = RemoteRequest.collect_response_data(mock_response)
        self.assertEqual(data.get('response_code'), mock_response.status_code)
        self.assertEqual(data.get('response_data'), mock_data)

    def test_collect_response_text_data(self):
        mock_response = Mock()
        mock_data = 'Test response'
        mock_response.status_code = 200
        mock_response.json = 1
        mock_response.text = mock_data
        data = RemoteRequest.collect_response_data(mock_response)
        self.assertEqual(data.get('response_code'), mock_response.status_code)
        self.assertEqual(data.get('response_data'), {'Message': mock_data})

    def test_collect_response_invalid_data(self):
        response = {'Message': 'Error: Could not reach remote address'}
        data = RemoteRequest.collect_response_data(None)
        self.assertEqual(data.get('response_code'), 500)
        self.assertEqual(data.get('response_data'), response)
