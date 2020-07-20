from stratatilities.auth import read_vault_secret


def get_redshift_dsn(vault_client):
    host = read_vault_secret(vault_client, "secret/staging/shared/DB_REDSHIFT_HOST")
    port = read_vault_secret(vault_client, "secret/staging/shared/DB_REDSHIFT_PORT")
    dbname = read_vault_secret(vault_client, "secret/staging/shared/DB_REDSHIFT_NAME")
    db_creds = read_vault_secret(
        vault_client, "database/creds/redshift-staging", vault_value_key=None
    )
    username = db_creds["username"].lower()
    password = db_creds["password"]
    template = "postgresql://{username}:{password}@{host}:{port}/{dbname}?keepalives=1"
    return template.format(
        username=username, password=password, host=host, port=port, dbname=dbname
    )


def get_rds_dsn(vault_client):
    host = read_vault_secret(vault_client, "secret/staging/shared/DB_DEFAULT_HOST",)
    port = read_vault_secret(vault_client, "secret/staging/shared/DB_DEFAULT_PORT",)
    dbname = read_vault_secret(vault_client, "secret/staging/shared/DB_DEFAULT_NAME",)
    db_creds = read_vault_secret(
        vault_client, "database/creds/rds-staging", vault_value_key=None,
    )
    username = db_creds["username"]
    password = db_creds["password"]
    template = "postgresql://{username}:{password}@{host}:{port}/{dbname}?keepalives=1"
    return template.format(
        username=username, password=password, host=host, port=port, dbname=dbname
    )
