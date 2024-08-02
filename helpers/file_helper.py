import logging
import os
from typing import Union

logger = logging.getLogger(__name__)


def get_base_path() -> Union[str, None]:
    operating_system = os.environ.get('OS')
    match operating_system:
        case "Windows":
            # return "../checkspod_files/" - This doesn't work with whisperx. Maybe works with custom?
            return "checkspod_files/"
        case "Mac":
            return "checkspod_files.nosync/"
        case "_":
            logger.critical("No valid operating system found")