import logging

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO  # You can change to DEBUG for more detailed logs

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

CELERYD_LOG_FORMAT = LOG_FORMAT
CELERYD_TASK_LOG_FORMAT = LOG_FORMAT
CELERYD_LOG_LEVEL = LOG_LEVEL
