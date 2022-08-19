from typing import Any, Dict, Union

from pydantic import (
    BaseSettings,
    PostgresDsn,
    validator,
)

class Settings(BaseSettings):
    PROJECT_NAME: str = 'FastAPI'
    DESCRIPTION: str = 'FastAPI'
    VERSION: str = '0.0.1'

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URI: Union[PostgresDsn, None] = None

    @validator('DATABASE_URI', pre=True)
    def assemble_db_connection(
        cls, value: Union[str, None], values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> str:
        if isinstance(value, str):
            return value
        
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path='/{0}'.format(values.get('DB_NAME')),
        )

    class Config(object):
        case_sensitive = True


settings = Settings()