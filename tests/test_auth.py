import os
try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

from stratatilities.auth import read_vault_secret, get_vault_client


@patch.dict(os.environ,{'VAULT_TOKEN':'token'})
def test_get_vault_client_env_variable():
    url = 'http://vault.example.com:8200'
    path = 'stratatilities.auth.'
    with patch(path + 'hvac') as hvac:

        client = get_vault_client(url)
        assert client == hvac.Client.return_value
        hvac.Client.assert_called_with(
            url=url,
            verify=False,
            token='token'
        )

def test_get_vault_client_iam():
    url = 'http://vault.example.com:8200'
    path = 'stratatilities.auth.'
    with patch(path + 'boto3.Session.get_credentials') as creds:
        with patch(path + 'hvac') as hvac:
            client = get_vault_client(url)
            assert client == hvac.Client.return_value
            hvac.Client.assert_called_with(
                url=url,
                verify=False,
            )
            creds.assert_called()
            client.auth_aws_iam.assert_called()

def test_read_vault_client():
    client = Mock()
    path = 'path/to/sekret'

    client.read.return_value = {
        'data': {
            'value': 'output'
        }
    }

    answer = read_vault_secret(client, path)
    assert answer == 'output'

    client.read.assert_called_with(path)

