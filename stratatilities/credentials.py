from stratatilities.auth import read_aws_secret
import getpass
from urllib.parse import quote


def get_redshift_dsn(username):
    host = read_aws_secret("health-prod-DB_REDSHIFT_HOST")
    port = "5439"
    # read_vault_secret(vault_client, "secret/staging/shared/DB_REDSHIFT_PORT")
    # not a secret stored in AWS for what used to be available in Vault
    dbname = read_aws_secret("health-prod-DB_REDSHIFT_NAME")

    username = username.lower()
    password = quote(getpass.getpass("Redshift Password:"))
    return f"""postgresql://{username}:{password}@{host}:{port}/{dbname}?keepalives=1"""
