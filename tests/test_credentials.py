from unittest.mock import patch, Mock, call

from stratatilities.credentials import get_redshift_dsn


def test_get_redshift_dsn():
    path = 'stratilities.credentials.read_vault_secret'
    with patch(path) as read_vault_secret:
        vault_client = Mock()
        read_vault_secret.return_value = [
            'host',
            'port',
            'dbname',
            {'username': 'USERNAME', 'password': 'password'},
        ]

        dsn = get_redshift_dsn(vault_client)
        # any capped chars in username must be lowered because redshift
        assert dsn == 'postgresql://username:password@host:port/dbname?keepalives=1'  # noqa
        calls = [
            call(vault_client, 'secret/staging/shared/DB_REDSHIFT_HOST'),
            call(vault_client, 'secret/staging/shared/DB_REDSHIFT_POST'),
            call(vault_client, 'secret/staging/shared/DB_REDSHIFT_NAME'),
            call(
                vault_client,
                'database/creds/redshift-staging',
                vault_value_key=None,
            ),
        ]
        read_vault_secret.assert_has_calls(calls)
