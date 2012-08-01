import os 
import sys
import logging

import django.core.handlers.wsgi 
import django.core.signals

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 


import fix_path


def log_exception(*args, **kwds):
    """Django signal handler to log an exception."""
    cls, err = sys.exc_info()[:2]
    logging.exception('Exception in request: %s: %s', cls.__name__, err)
      
# Log all exceptions detected by Django.
django.core.signals.got_request_exception.connect(log_exception)

app = django.core.handlers.wsgi.WSGIHandler()
