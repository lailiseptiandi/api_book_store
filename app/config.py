from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()