"""
Defines a number of log level attributes and :class:`LegacySyslogger` to
carry out the real work.

This module should not be used for new work, but is provided to smooth
the transition from *tclutils.log*.

By default, log entries are sent to standard output and the system logger.

Four valid log level constants are provided at the module level:

* **ERROR** -- a problem that means execution cannot, or should not continue
* **WARNING** -- an unexpected situtation but execution will continue
* **INFO** -- informational output not indicative of a problem e.g. progress messages
* **DEBUG** -- a message that should only be emitted when debugging code

These constants may be used anywhere that a *level* is expected by
:class:`LegacySyslogger`.
"""

import os
import sys
import syslog

# Log levels
ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3
LOGLEVELS = (ERROR, WARNING, INFO, DEBUG)
LOGPREFIX = {
    ERROR: 'E',
    WARNING: 'W',
    INFO: 'I',
    DEBUG: 'D',
}


class LegacySyslogger:
    """
    An object that looks a bit like a Python logging object
    so that we can transition more easily later.

    Example usage:

    >>> s = LegacySyslogger()
    >>> # Long hand:
    >>> s.log(WARNING, 'Unable to biggle')
    W: Unable to biggle
    >>> # Short hand:
    >>> s.warning('Could not frob; continuing')
    W: Could not frob, continuing
    >>> s.error('Abandon ship, all ye who run this')
    E: Abandon ship, all ye who run this
    """

    # minimum log level to send
    _log_level = DEBUG
    # log to stdout?
    _log_to_stdout = True,
    # log to syslog?
    _log_to_syslog = True,
    # log tag
    _syslog_name = None

    @property
    def log_level(self):
        """
        Minimum level at which to emit a log entry
        """
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        if value in LOGLEVELS:
            self._log_level = value
        else:
            raise ValueError('%s not an acceptable log level' % value)

    @property
    def log_to_stdout(self):
        """
        Whether to log to *stdout* (*True* or *False*)
        """
        return self._log_to_stdout

    @log_to_stdout.setter
    def log_to_stdout(self, value):
        if value in (True, False):
            self._log_to_stdout = value
        else:
            raise ValueError('log_to_stdout must be True or False')

    @property
    def log_to_syslog(self):
        """
        Whether to log to *syslog* (*True* or *False*)
        """
        return self._log_to_stdout

    @log_to_syslog.setter
    def log_to_syslog(self, value):
        if value in (True, False):
            self._log_to_syslog = value
        else:
            raise ValueError('log_to_stdout must be True or False')

    @property
    def syslog_name(self):
        """
        Log tag used in syslog messages (string)
        """
        return self._syslog_name

    @syslog_name.setter
    def syslog_name(self, value):
        self._syslog_name = value

    def log(self, level, msg):
        """
        Print a message if its level is equal or less than
        the filter level. Depending on configuration, the message
        may be emitted to *syslog* or to *stdout* or both.

        :param int level: Log message level
        :param str msg: Log message text
        """

        if level <= self.log_level:
            # Add prefix to message
            if level in LOGPREFIX:
                msg = LOGPREFIX[level] + ": " + msg
            if self.log_to_stdout:
                sys.stderr.write(msg + "\n")
            if self.log_to_syslog:
                if self.syslog_name:
                    syslog.syslog("%s: %s" % (self.syslog_name, msg))
                else:
                    syslog.syslog("%s" % (msg))

    def debug(self, msg):
        """Shorthand for :func:`log(DEBUG, msg)`"""
        self.log(DEBUG, msg)

    def info(self, msg):
        """Shorthand for *log(INFO, msg)*"""
        self.log(INFO, msg)

    def warning(self, msg):
        """Shorthand for *log(WARNING, msg)*"""
        self.log(WARNING, msg)

    def error(self, msg):
        """Shorthand for *log(ERROR, msg)*"""
        self.log(ERROR, msg)