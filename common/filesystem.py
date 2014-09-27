"""
Wrapper for loading templates from the filesystem.
"""

import settings

import logging
import os, zlib
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils._os import safe_join

from google.appengine.api import memcache
from google.appengine.ext import db

all_templates = memcache.get('templates') or {}

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')

class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        if not template_dirs:
            template_dirs = settings.TEMPLATE_DIRS
        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, template_name)
            except UnicodeDecodeError:
                # The template dir name was a bytestring that wasn't valid UTF-8.
                raise
            except ValueError:
                # The joined path was located outside of this particular
                # template_dir (it might be inside another one, so this isn't
                # fatal).
                pass

    def load_template_source(self, template_name, template_dirs=None):
        
        result = ''
        try:            
            
            if DEBUG == False:
                result = all_templates[template_name]
            
                if result:
                    #logging.info("from memory: %s", template_name)
                    return (result, template_name)
        except:
            pass                            
                         
        
        tried = []
        for filepath in self.get_template_sources(template_name, template_dirs):
            try:
                 
                file = open(filepath)

                try:                 
                    result = file.read().decode('utf-8')

                    try:
                    
                        if DEBUG == False:
                            all_templates[template_name] = result
                            memcache.set('templates', all_templates)
                            logging.info("saved disk: %s", template_name)                        
                           
                    except:
                        pass                        
                    return (result, filepath)
                finally:
                    file.close()
            except IOError:
                tried.append(filepath)
        if tried:
            error_msg = "Tried %s" % tried
        else:
            error_msg = "Your TEMPLATE_DIRS setting is empty. Change it to point to at least one template directory."
        raise TemplateDoesNotExist(error_msg)
    load_template_source.is_usable = True

_loader = Loader()

def load_template_source(template_name, template_dirs=None):
    # For backwards compatibility
    import warnings
    warnings.warn(
        "'django.template.loaders.filesystem.load_template_source' is deprecated; use 'django.template.loaders.filesystem.Loader' instead.",
        PendingDeprecationWarning
    )
    return _loader.load_template_source(template_name, template_dirs)
load_template_source.is_usable = True
