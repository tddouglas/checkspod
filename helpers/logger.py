import logging
import logging.config
import coloredlogs


def setup_logging(log_level):
    logging_config = {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': log_level
            },
            # Use the below to log to a file. Currently just logging to command line
            # 'file': {
            #     'class': 'logging.FileHandler',
            #     'formatter': 'standard',
            #     'level': 'INFO',
            #     'filename': 'app.log',
            # },
        },
        'root': {
            # 'handlers': ['console', 'file'], #  Add 'file' handler if we want to log to file
            'handlers': ['console'],
            'level': log_level
        }
    }

    logging.config.dictConfig(logging_config)
    coloredlogs.install(level=log_level)
