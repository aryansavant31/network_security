import logging
from datetime import datetime
import os

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(log_path, exist_ok=True)

logger = logging.basicConfig(
    filename=log_path,
    format="[ %(asctime) ] %(lineno)d %(name)s - %(levelname)s -%(message)s",
    level=logging.INFO
)