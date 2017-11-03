from mock import patch, Mock

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

