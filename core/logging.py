import os
import logging.config
import logging
import yaml

core_logging_setup = False


def __setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOGGING_CONFIG'):
    """Setup logging configuration.
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    global core_logging_setup
    core_logging_setup = True


def get_logger(name):
    if core_logging_setup is False:
        __setup_logging()
    return logging.getLogger(name)


class LoggerMixin(object):
    """Provides a logger attribute for any class, named for the class module.

    Usage:

    ```
    class Foo(LoggerMixin):

    """

    __logger = None

    @property
    def logger(self):
        """Return logger instance, named for the module and class."""
        if self.__logger is None:
            name = '.'.join([
                self.__module__,
                self.__class__.__name__
            ])
        self.__logger = get_logger(name)

        return self.__logger
