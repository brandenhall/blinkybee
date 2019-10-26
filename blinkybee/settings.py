HTTP_PORT = 8080
WEB_ROOT = 'web'
FRAME_RATE = 30
PIXEL_COUNT = 87

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(asctime)s.%(msecs).03d %(levelname)s [%(module)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'root': {
        'handlers': ['console', ],
        'propagate': True,
        'level': 'WARNING',
    },
    'loggers': {
        'conductor': {
            'handlers': ['console', ],
            'propagate': False,
            'level': 'DEBUG',
        }
    },
}
