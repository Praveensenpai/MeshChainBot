import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> - <level>{message}</level>",
    enqueue=True,
)
logger.level("INFO", color="<blue>")
