import logging

class LoggableObject(object):
    @property
    def log(self):
        log = getattr(self, '_logger', None)
        if log is None:
            log = self._logger = logging.getLogger('%s.%s' % (self.__class__.__module__, self.__class__.__name__))
        return log
