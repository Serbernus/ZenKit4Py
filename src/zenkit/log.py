__all__ = [
    "LogLevel",
    "set_logger",
    "set_logger_default",
]

from ctypes import c_void_p, c_int, c_char_p, CFUNCTYPE
from enum import IntEnum
from typing import Callable

from zenkit._core import DLL

_Logger = CFUNCTYPE(None, c_void_p, c_int, c_char_p, c_char_p)
_LOGGER: _Logger | None = None


class LogLevel(IntEnum):
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3
    TRACE = 4


def set_logger(level: LogLevel, cb: Callable[[LogLevel, str, str], None]) -> None:
    logger = _Logger(
        lambda _, lvl, name, message: cb(
            LogLevel(lvl), name.decode("utf-8"), message.decode("utf-8")
        )
    )

    global _LOGGER
    _LOGGER = logger

    DLL.ZkLogger_set.restype = None
    DLL.ZkLogger_set(c_int(level.value), _LOGGER, c_void_p(None))


def set_logger_default(level: LogLevel) -> None:
    DLL.ZkLogger_setDefault.restype = None
    DLL.ZkLogger_setDefault(c_int(level.value))
