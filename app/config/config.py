import os
import sys
from pathlib import Path
from typing import Any, Optional

import pydantic
from dotenv import dotenv_values
from loguru import logger as base_logger


def get_env_dict(env_dir: Optional[Path]):
    env_shared = dotenv_values(str(env_dir / "shared.env"))
    env_secret = dotenv_values(str(env_dir / "secret.env"))
    env_dict = {**env_shared, **env_secret, **os.environ}
    env_dict = {k: v for k, v in env_dict.items() if ("<secret>" not in v) or ("<project>" not in v)}
    return env_dict


def get_db_url(env_dict: dict[str, Any], is_asnc: bool = True) -> str:

    use_global = pydantic.parse_obj_as(bool, env_dict.get("USE_GLOBAL", "True"))

    prefix = "postgresql+asyncpg" if is_asnc else "postgresql"
    user = env_dict.get("DB_USER")
    password = env_dict.get("DB_PASSWORD")
    host = env_dict.get("DB_HOST_GLOBAL") if use_global else env_dict.get("DB_HOST_LOCAL")
    port = env_dict.get("DB_PORT")
    db_name = env_dict.get("DB_NAME")

    return f"{prefix}://{user}:{password}@{host}:{port}/{db_name}"


class Rotator:
    def __init__(self, *, size):
        self._size_limit = size

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        return False


def get_logger(logging_level: str, log_dir: Optional[Path] = None, logging_dir_level: str = "DEBUG"):
    base_logger.remove()
    base_logger.add(sys.stderr, level=logging_level)

    # если указать путь, то логи будут записываться не только в stderr
    if log_dir:
        rotator = Rotator(size=5e8)
        base_logger.add(
            log_dir / "{time}.log",
            level=logging_dir_level,
            rotation=rotator.should_rotate,
        )

    return base_logger


env_dict = get_env_dict(Path(__file__).parents[0])

db_url = get_db_url(env_dict)
db_url_alembic = get_db_url(env_dict, is_asnc=False)

logger = get_logger(
    logging_level=env_dict.get("LOGGING_LEVEL", "INFO"),
    log_dir=Path(env_dict.get("LOG_DIR")) if env_dict.get("LOG_DIR") else None,
    logging_dir_level=env_dict.get("LOGGING_DIR_LEVEL", "DEBUG"),
)
