import os
import os
from pathlib import Path
import hvac
from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    VAULT_ADDR: str = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
    VAULT_TOKEN: str = os.getenv("VAULT_TOKEN", "")
    VAULT_PATH: str = os.getenv("VAULT_PATH", "")
    SECRETS: dict = {}

    def load_vault_secrets(self):
        client = hvac.Client(url=self.VAULT_ADDR, token=self.VAULT_TOKEN)
        if not client.is_authenticated():
            raise Exception("Vault authentication failed")

        secret = client.secrets.kv.v2.read_secret_version(path=self.VAULT_PATH)["data"]["data"]
        self.SECRETS = secret

settings = Settings()
settings.load_vault_secrets()
