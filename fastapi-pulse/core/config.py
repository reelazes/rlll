from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class ApiPrefix(BaseModel):
    prefix: str = "/api"

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        cache_strings=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth_jwt: AuthJWT = AuthJWT()



settings = Settings()
