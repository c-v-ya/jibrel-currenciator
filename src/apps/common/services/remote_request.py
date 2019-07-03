import json
import logging
from traceback import format_exc

import requests

from src.apps.common.enums import RequestMethod
from src.apps.common.enums import RequestStatus

SUCCESS_CODES = [200, 201, 202, 203]

log = logging.getLogger(__name__)


class RemoteRequest:
    allowed_response_codes = [200, 201, 203, 400, 401, 403]

    def __init__(self, url, headers, basic_auth, method, request_data,
                 response_data=None, status=None, status_code=None,
                 created_date=None):
        self.url = url
        self.headers = headers
        self.basic_auth = basic_auth
        self.method = method
        self.request_data = request_data
        self.response_data = response_data
        self.status = status
        self.status_code = status_code
        self.created_date = created_date

        log.info('{} request to {} with data {}'.format(
            method, url,
            json.dumps(request_data, ensure_ascii=False, indent=2))
        )

    @property
    def json(self):
        if isinstance(self.response_data, dict) \
                or isinstance(self.response_data, list):
            return self.response_data
        else:
            return json.loads(self.response_data)

    @property
    def _response(self):
        response = self.send_request()
        return self.collect_response_data(response)

    def send_request(self):
        try:
            auth = tuple(self.basic_auth) if self.basic_auth else None
            if self.method == RequestMethod.GET:
                response = requests.get(self.url, params=self.request_data,
                                        headers=self.headers, auth=auth)
            else:
                if self.headers.get('Content-type') == 'application/json':
                    response = requests.post(self.url, json=self.request_data,
                                             headers=self.headers, auth=auth)
                else:
                    response = requests.post(self.url, data=self.request_data,
                                             headers=self.headers, auth=auth)
        except requests.exceptions.RequestException as e:
            log.error(format_exc())
            return e

        return response

    @classmethod
    def collect_response_data(cls, response):
        try:
            response_code = response.status_code
            try:
                response_data = response.json()
            except Exception:
                response_data = {'Message': response.text} \
                    if response_code in SUCCESS_CODES \
                    else {'Message': 'Error: Unknown status of response.'}
        except AttributeError:
            log.error(format_exc())
            response_code = 500
            response_data = {
                'Message': 'Error: Could not reach remote address'}

        return {
            'response_code': response_code,
            'response_data': response_data,
        }

    @classmethod
    def send(cls, url, data, method=RequestMethod.POST, headers=None,
             basic_auth=None):
        if headers is None:
            headers = {'Content-type': 'application/json'}
        r_request = cls(url=url, headers=headers, method=method,
                        request_data=data, basic_auth=basic_auth)

        response = r_request._response

        r_request.response_data = response.get('response_data')
        r_request.status_code = response.get('response_code')
        if r_request.status_code not in SUCCESS_CODES:
            r_request.status = RequestStatus.FAIL

        r_request.status = RequestStatus.SUCCESS

        log.info('{} to {} returned {} with status {}'.format(
            method, url,
            json.dumps(r_request.response_data, ensure_ascii=False, indent=2),
            r_request.status_code
        ))

        return r_request
