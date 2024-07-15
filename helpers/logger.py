import logging
import logging.config


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
                'level': log_level,
            },
            # Use the below to log to a file. Currently just logging to command line
            # 'file': {
            #     'class': 'logging.FileHandler',
            #     'formatter': 'standard',
            #     'level': 'INFO',
            #     'filename': 'app.log',
            # },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True
            },
            'my_module': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }

    logging.config.dictConfig(logging_config)
