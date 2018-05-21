import logging

from face.common.utils import makedirs
from face.common import constants as consts

LOG_FORMATTER = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s %(filename)s:%(lineno)d %(message)s'
    )

LOG_STREAM_HANDLER = logging.StreamHandler()
LOG_STREAM_HANDLER.setFormatter(LOG_FORMATTER)
LOG_STREAM_HANDLER.setLevel(logging.INFO)

makedirs(consts.LOG_DIR)
LOG_FILE_HANDLER = logging.FileHandler(consts.LOG_FILE)
LOG_FILE_HANDLER.setFormatter(LOG_FORMATTER)
LOG_FILE_HANDLER.setLevel(logging.DEBUG)

logging.root.addHandler(LOG_STREAM_HANDLER)
logging.root.addHandler(LOG_FILE_HANDLER)
