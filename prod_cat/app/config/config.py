import os
import sys
import traceback
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Optional, Any

from dotenv import dotenv_values
from loguru import logger as base_logger


def get_env_dict(env_dir: Optional[Path]):
    env_shared = dotenv_values(str(env_dir / "shared.env"))
    env_secret = dotenv_values(str(env_dir / "secret.env"))
    env_dict = {**env_shared, **env_secret, **os.environ}
    env_dict = {
        k: v
        for k, v in env_dict.items()
        if ("<secret>" not in v) or ("<project>" not in v)
    }
    return env_dict


def get_db_url(env_dict: dict[str, Any]) -> str:
    # postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName
    return f"postgresql+asyncpg://{env_dict.get('DB_USER')}:{env_dict.get('DB_PASSWORD')}@{env_dict.get('DB_HOST')}:{env_dict.get('DB_PORT')}/{env_dict.get('DB_NAME')}"


class Rotator:
    def __init__(self, *, size):
        self._size_limit = size

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        return False


def get_logger(
    logging_level: str, log_dir: Optional[Path] = None, logging_dir_level: str = "DEBUG"
):
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
logger = get_logger(
    logging_level=env_dict.get("LOGGING_LEVEL", "INFO"),
    log_dir=Path(env_dict.get("LOG_DIR", None)),
    logging_dir_level=env_dict.get("LOGGING_DIR_LEVEL", "DEBUG"),
)


def logger_dec(func_info: str) -> callable:
    """
    Add start/finish logging to function\n
    Parameters
    ----------
    func_info : str
        string which will be displayed in the logs. For example "finish {func_info}"
    """

    def decorator(func: callable) -> callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # get real file and line what was called
            file = "/".join(traceback.extract_stack()[-2].filename.split("/")[-2:])
            function_name = func.__name__
            line = traceback.extract_stack()[-2].lineno
            
            patched_logger = logger.patch(lambda r: r.update(function=function_name, name=file, line=line))

            start_time = datetime.now()
            
            patched_logger.info(f"start {func_info}")

            res = await func(*args, **kwargs)

            patched_logger.info(f"finish {func_info} ({datetime.now() - start_time})")

            return res

        return wrapper

    return decorator
