import base64
import getpass
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

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    pass

logger = logging.getLogger(__name__)


def headers_to_go_style(headers):
    retval = {}
    for k, v in headers.items():
        if isinstance(v, bytes):
            retval[k] = [str(v, "ascii")]
        else:
            retval[k] = [v]
    return retval


def get_token(
    vault_addr, iam_role_name, iam_request_body, iam_request_url, iam_request_headers
):
    payload = {
        "role": iam_role_name,
        "iam_http_request_method": "POST",
        "iam_request_url": iam_request_url,
        "iam_request_body": iam_request_body,
        "iam_request_headers": iam_request_headers,
    }
    headers = {"content-type": "application/json"}
    response = requests.post(
        "{}/v1/auth/aws/login".format(vault_addr),
        verify=False,
        timeout=5,
        data=json.dumps(payload),
        headers=headers,
    )
    response_json = response.json()
    return response_json["auth"]["client_token"]


def request_vault_token(vault_addr):
    """ Requests a Vault Token from an IAM Role """
    session = boto3.session.Session()
    client = session.client("sts")
    endpoint = client._endpoint
    role_name = client.get_caller_identity()["Arn"].split("/")[1]
    logger.debug('Requesting vault token with IAM role name "%s"', role_name)

    operation_model = client._service_model.operation_model("GetCallerIdentity")
    request_dict = client._convert_to_request_dict({}, operation_model)

    awsIamServerId = urlparse(vault_addr).hostname
    request_dict["headers"]["X-Vault-awsiam-Server-Id"] = awsIamServerId

    logger.debug(
        'Creating request with request_dict "%s" and operation_model "%s"',
        request_dict,
        operation_model,
    )
    request = endpoint.create_request(request_dict, operation_model)
    return get_token(
        vault_addr,
        role_name,
        str(base64.b64encode(request.body.encode("ascii")), "ascii"),
        str(base64.b64encode(request.url.encode("ascii")), "ascii"),
        str(
            base64.b64encode(
                bytes(json.dumps(headers_to_go_style(dict(request.headers))), "ascii")
            ),
            "ascii",
        ),
    )


def get_vault_client(vault_addr=os.environ.get("VAULT_ADDR")):
    vault_token = os.environ.get("VAULT_TOKEN", None)
    if not vault_token:
        vault_token = request_vault_token(vault_addr)
    logger.debug("vault token: %s", vault_token)
    return hvac.Client(url=vault_addr, verify=False, token=vault_token)


def get_vault_client_via_ldap(
    username, mount_point="ldap", vault_addr=os.environ.get("VAULT_ADDR")
):
    """ Return an authenticated vault client via LDAP.

    Password will be acquired via `getpass.getpass`. Services should
    use `get_vault_client` with IAM privileges.

    InvalidRequest is raised from an incorrect password being entered
    """
    client = hvac.Client(url=vault_addr)
    # with an incorrect password, an InvalidRequest is raised
    client.auth.ldap.login(
        username=username,
        password=getpass.getpass("LDAP Password:"),
        mount_point=mount_point,
    )
    assert client.is_authenticated(), "Client is not authenticated!"
    return client


def return_token(vault_addr=os.environ.get("VAULT_ADDR")):
    vault_token = os.environ.get("VAULT_TOKEN", None)
    if not vault_token:
        vault_token = request_vault_token(vault_addr)
    logger.debug("vault token: %s", vault_token)
    return vault_token


def read_vault_secret(vault_client, path_to_secret, vault_value_key="value"):
    """ Read a vault secret given a {vault_client} and {path_to_secret}

    If the secret is "complex", in that it's more than just key/value,
    then passing `vault_value_key=None` will return the blob from vault
    and you can do w/ it as you wish, otherwise vault_value_key is used
    to access the object returned in response['data']
    """
    vault_value = None
    try:
        if vault_value_key is None:
            vault_value = vault_client.read(path_to_secret)["data"]
        else:
            vault_value = vault_client.read(path_to_secret)["data"][vault_value_key]
    except TypeError:
        pass
    return vault_value
