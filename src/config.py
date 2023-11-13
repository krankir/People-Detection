from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Здесь весь конфиг. Часть берется с виртуального окружения. """
    bucket_name: str
    minio_host: str
    minio_password: str
    minio_user: str
    minio_port: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    amqp_cs: str

    class Config:
        env_file = '.env'


settings = Settings()


