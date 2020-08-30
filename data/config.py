from pathlib import Path
from logging import ERROR, INFO, DEBUG

DATA_PATH = Path().cwd() / "data"
DATA_PATH.mkdir(parents=True, exist_ok=True)

FILE_PATH = DATA_PATH / "task.json"
DB_PATH = DATA_PATH / "database.db"

OVERALL_LOG_LEVEL = DEBUG

LOGGER_NAME = "recipe_service"
LOGGER_LEVEL = DEBUG
LOGGER_FORMAT = "%(asctime)s - %(levelname)-5s - %(message)s"  # %(filename)-11s:%(lineno)3d
LOG_PATH = DATA_PATH / "logs" / "log.log"
LOG_PATH.mkdir(parents=True, exist_ok=True)
