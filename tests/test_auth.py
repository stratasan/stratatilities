try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

from stratatilities.auth import read_vault_secret, get_vault_client


def test_get_vault_client():
    url = 'http://vault.example.com:8200'
    path = 'stratatilities.auth.'
    with patch(path + 'request_vault_token') as request_vault:
        with patch(path + 'hvac') as hvac:
            request_vault.return_value = 'token'

            client = get_vault_client(url)
            assert client == hvac.Client.return_value
            hvac.Client.assert_called_with(
                url=url,
                verify=False,
                token=request_vault.return_value
            )


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

    # If we're expecting a complex value in 'data'
    complex_value = {
        'complex': 'values',
        'another': 'key'
    }
    client.read.return_value = {
        'data': complex_value
    }
    # then passing vault_value_key=None will make the funtion
    # return 'data' and not do a further key access
    answer = read_vault_secret(client, path, vault_value_key=None)
    assert answer == complex_value
