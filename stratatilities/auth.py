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
try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    pass

logger = logging.getLogger(__name__)


def get_vault_client(vault_addr=os.environ.get('VAULT_ADDR', 'https://vault.stratasan.com:8200')):
    vault_token = os.environ.get('VAULT_TOKEN', None)
    vault_client = None
    if vault_token:
        vault_client = hvac.Client(url=vault_addr, verify=False, token=vault_token)
    else:
        aws_credentials = boto3.Session().get_credentials()
        vault_client = hvac.Client(url=vault_addr, verify=False)
        vault_client.auth_aws_iam(aws_credentials.access_key, aws_credentials.secret_key, aws_credentials.token)
        vault_token = vault_client.token
    logger.debug('vault token: %s', vault_token)
    return vault_client


def return_token(vault_addr=os.environ.get('VAULT_ADDR')):
    vault_token = os.environ.get('VAULT_TOKEN', get_vault_client(vault_addr).token)
    logger.debug('vault token: %s', vault_token)
    return vault_token


def read_vault_secret(vault_client, path_to_secret,vault_value_key='value'):
    vault_value = None
    try:
        vault_value = vault_client.read(path_to_secret)['data'][vault_value_key]
    except TypeError:
        pass
    return vault_value
