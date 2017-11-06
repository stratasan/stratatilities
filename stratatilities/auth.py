import base64
import json
import logging
import os
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import boto3
import hvac
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = logging.getLogger(__name__)


def headers_to_go_style(headers):
    retval = {}
    for k, v in headers.items():
        if isinstance(v, bytes):
            retval[k] = [str(v, 'ascii')]
        else:
            retval[k] = [v]
    return retval


def get_token(vault_addr,
              iam_role_name,
              iam_request_body,
              iam_request_url,
              iam_request_headers):
    payload = {
        "role": iam_role_name,
        "iam_http_request_method": "POST",
        "iam_request_url": iam_request_url,
        "iam_request_body": iam_request_body,
        "iam_request_headers": iam_request_headers,
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(
        '{}/v1/auth/aws/login'.format(vault_addr),
        verify=False,
        timeout=5,
        data=json.dumps(payload),
        headers=headers
    )
    return response.json()['auth']['client_token']


def request_vault_token(vault_addr):
    """ Requests a Vault Token from an IAM Role """
    session = boto3.session.Session()
    client = session.client('sts')
    endpoint = client._endpoint
    role_name = client.get_caller_identity()['Arn'].split('/')[1]

    operation_model = client._service_model.operation_model('GetCallerIdentity')
    request_dict = client._convert_to_request_dict({}, operation_model)

    awsIamServerId = urlparse(vault_addr).hostname
    request_dict['headers']['X-Vault-awsiam-Server-Id'] = awsIamServerId

    request = endpoint.create_request(request_dict, operation_model)
    return get_token(
        vault_addr,
        role_name,
        str(base64.b64encode(request.body.encode('ascii')), 'ascii'),
        str(base64.b64encode(request.url.encode('ascii')), 'ascii'),
        str(base64.b64encode(bytes(json.dumps(headers_to_go_style(dict(request.headers))), 'ascii')), 'ascii')
    )


def get_vault_client(vault_addr):
    vault_token = request_vault_token(vault_addr)
    logger.debug('vault token: %s', vault_token)
    return hvac.Client(url=vault_addr, verify=False, token=vault_token)


def read_vault_secret(vault_client, path_to_secret):
    return vault_client.read(path_to_secret)['data']['value']
