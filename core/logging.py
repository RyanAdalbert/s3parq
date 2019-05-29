import os
import logging.config
import logging
import yaml

core_logging_setup = False
from core.helpers.project_root import ProjectRoot
from core.constants import LOGGING_CONFIG


def __setup_logging():
    """Setup logging configuration.

    This method is automatically invoked by get_logger, and shouldn't need to be called directly.
    """
    config_file = os.path.join(ProjectRoot().get_path(), 'config', LOGGING_CONFIG)

    if os.path.exists(config_file):
        with open(config_file, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        raise FileNotFoundError(f"Logging configuration file does not exist at {config_file}")

    global core_logging_setup
    core_logging_setup = True


def get_logger(name: str) -> logging.Logger:
    if core_logging_setup is False:
        __setup_logging()
    return logging.getLogger(name)


class LoggerMixin(object):
    """Provides a logger attribute for any class, named for the class module.

    Usage:

    ```
    class Foo(LoggerMixin):
        def bar(self):
            self.logger.debug("Log this debug message")
`   ```
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


class LoggerSingleton(object):
    """ logger attribute class for use in a procdeural module.
    Usage:
    
    ```
    logger = LoggerSingleton().logger
    
    ## some code later.. 
    logger.debug("this is a debug message!")
    ```
    """
    __logger = None
    @property
    def logger(self)-> logging.Logger:
        if self.__logger is None:
            self.__logger = get_logger(__name__)       
        
        return self.__logger       
