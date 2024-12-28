import logging
import pathlib
from logging.handlers import RotatingFileHandler

import appdirs

from ._version import __version__

USER_LOG_DIR = pathlib.Path(appdirs.user_log_dir(__package__, version=__version__))
USER_LOG_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_LOGGING_LEVEL = logging.DEBUG
_formatter = logging.Formatter(
    '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S')

_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(DEFAULT_LOGGING_LEVEL)
_stream_handler.setFormatter(_formatter)

_file_handler = RotatingFileHandler(USER_LOG_DIR / f'{__package__}.log')
_file_handler.setLevel(logging.DEBUG)  # log everything to file!
_file_handler.setFormatter(_formatter)

logger = logging.getLogger(__package__)
logger.addHandler(_stream_handler)
logger.addHandler(_file_handler)

logger = logging.getLogger(__package__)
logger.addHandler(_stream_handler)
logger.addHandler(_file_handler)

from .gldb import GenericLinkedDatabase
from gldb.stores.datastore import DataStore

__all__ = ['GenericLinkedDatabase', 'RDFStore', 'DataStore']
