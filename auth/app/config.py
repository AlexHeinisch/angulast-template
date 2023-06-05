from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    access_token_algo: str = 'RS256'
    access_token_pubkey: str = ''

    class Config:
        secrets_dir = './secrets'

settings = Settings()
