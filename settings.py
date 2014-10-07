#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Google Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -*- coding: utf-8 -*-

import os.path

#from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _
#from djangoappengine.settings_base import *
###
# Django related settings
###
        

template = {}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Nikita', 'nikita.grachev@gmail.com'),
)


CSS_VERSION = '1021'

MANAGERS = ADMINS

# This stuff is always going to be the same for an App Engine instance
#DATABASE_ENGINE = 'sqlite3'  # 'appengine' is the only supported engine
#DATABASE_NAME = ''             # Not used with appengine
#DATABASE_USER = ''             # Not used with appengine
#DATABASE_PASSWORD = ''         # Not used with appengine
#DATABASE_HOST = ''             # Not used with appengine
#DATABASE_PORT = ''             # Not used with appengine

# The appengine_django code doesn't care about the address of memcached
# because it is a built in API for App Engine
#CACHE_BACKEND = 'memcached://'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGE_CODE_RUS = 'ru'

LANGUAGE_CODE = 'ru'#'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ('ru', (u'Русский')),
    #('en-us', ('English')),

)


LANGUAGE_CODE_FB = 'ru_RU'

LANGUAGES_FB = (
    # ('en-us', ('en_US')),
    ('ru', ('ru_RU')), 
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'I AM SO SECRET'

if DEBUG:
    TEMPLATE_LOADERS = (
        (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
    )
else:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )
    
    
AUTHENTICATION_BACKENDS = (
    #'socialregistration.auth.FacebookAuths',
)


MIDDLEWARE_CLASSES = (
    #'django.middleware.csrf.CsrfViewMiddleware',
        
    #'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    
    
    #'middleware.domain.DomainMiddleware',
    #'middleware.auth.AuthenticationMiddleware',
    #'middleware.exception.ExceptionMiddleware',
    #'middleware.cache.CacheMiddleware',
    #'middleware.strip_whitespace.WhitespaceMiddleware',
    #'middleware.profile.ProfileMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',   
    'common.middleware.UserLocation',         
    'common.middleware.UserAccess',   
    
    #'django.middleware.http.ConditionalGetMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    #'socialregistration.middleware.FacebookMiddleware',
    #'social_auth.middleware.SocialAuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

# Where the templates live, you probably don't want to change this unless you
# know what you're doing
TEMPLATE_DIRS = (
    os.path.dirname(__file__),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    #'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'common.context_processors.settings',
    
    
    #'common.context_processors.user',
    #'common.context_processors.flash',
    #'common.context_processors.components',

    #'django.contrib.auth.context_processors.auth',
    #'django.core.context_processors.request',

    'django.core.context_processors.i18n',

)

# Only apps under INSTALLED_APPS will be automatically tested via
# `python manage.py test` and the profiling code takes this list into
# account while filtering calls
INSTALLED_APPS = (
     #'appengine_django',
     #'djangoappengine',
     #'djangotoolbox',
     #'django.contrib.auth',
     #'django.contrib.contenttypes',
     #'django.contrib.sessions',
     #'django.contrib.sites',
     'common',
     #'actor',
     #'api',
     #'channel',
     #'explore',
     #'join',
     #'flat',
     #'login',
     #'front',
     #'invite',
     #'install',
     #'confirm',
     #'components',
     #'socialregistration',
)


GOOGLE_AUTHORIZE_URL = "http://www.onarena.com/authsub"
GOOGLE_CONSUMER_KEY = "www.onarena.com"
GOOGLE_CONSUMER_SECRET = "yFZOJYF8EtEJyFHzplwEiw9k"


TWITTER_CONSUMER_KEY = "g7ajf7OPlUzhMM9JBPk3ZQ"
TWITTER_CONSUMER_SECRET = "MCKHvJquCldbTjLG3rCwyVwWhsQkaX1X8JQy83dDHQ"
TWITTER_CONSUMER_SECRET_KEY = "MCKHvJquCldbTjLG3rCwyVwWhsQkaX1X8JQy83dDHQ"
TWITTER_REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
TWITTER_ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
TWITTER_AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize"
TWITTER_AUTHORIZATION_URL = "https://api.twitter.com/oauth/authorize"
TWITTER_API_URL = "http://api.twitter.com/1/users/show.json?user_id=%s"

VKONTAKTE_APP_ID = "XXXX"
VKONTAKTE_API_KEY = "XXXX"
VKONTAKTE_SECRET_KEY = "XXXXXXXXX"




# We override the default test runner so that we can be Totally Awesome
#TEST_RUNNER = 'common.test.runner.run_tests'


####
#
# Below this is custom for Jaiku Engine (not related to Django)
#
####


# This is a dynamic setting so that we can check whether we have been run
# locally, it is used mainly for making special testing-only tweaks. Ideally
# we wouldn't need this, but the alternatives so far have been tricky.
#MANAGE_PY = os.path.exists('manage.py')

# This is the name of the site that will be used whenever it refers to itself
SUPPORT_CHANNEL = 'support'

# This is the colloquial name for an entry, mostly used for branding purposes
POST_NAME = 'Post'

# This is the name of the root user of the site
ROOT_NICK = 'nikita.grachev@gmail.com'


# This is the domain where this is installed on App Engine. It will be
# necessary to know this if you plan on enabling SSL for login and join.
GAE_DOMAIN = 'cometiphrd.appspot.com'

# Enabling this means we expect to be spending most of our time on a
# Hosted domain
HOSTED_DOMAIN_ENABLED = False

# This is the domain you intend to serve your site from, when using hosted
# domains. If SSL is enabled for login and join those requests will still
# go to the GAE_DOMAIN above.
HOSTED_DOMAIN = ''

# App Engine requires you to serve with a subdomain
DEFAULT_HOSTED_SUBDOMAIN = 'www'

# DOMAIN will be used wherever a url to this site needs to be created
# NS_DOMAIN will be used as the domain part of actor identifiers.
# Note that changing this once you have deployed the site will likely result
# in catastrophic failure.
if HOSTED_DOMAIN_ENABLED:
    DOMAIN = '%s.%s' % (DEFAULT_HOSTED_SUBDOMAIN, HOSTED_DOMAIN)
else:
    DOMAIN = GAE_DOMAIN




# Subdomains aren't supported all that nicely by App Engine yet, so you
# probably won't be able to enable WILDCARD_SUBDOMAINS below, but you can
# still set up your app to use some of the static subdomains below.
# Subdomains are ignored unless HOSTED_DOMAIN_ENABLED is True.
SUBDOMAINS_ENABLED = False
WILDCARD_USER_SUBDOMAINS_ENABLED = False

# These are defined as { subdomain : url_conf, ...}
INSTALLED_SUBDOMAINS = {
    'api': 'api.urls',  # api-only urlconf
    'm': 'urls',          # default urlconf, but allow the subdomain
    }

# Enable SSL support for login and join, if using HOSTED_DOMAIN_ENABLED
# this means you will be redirecting through https://GAE_DOMAIN/login
# and https://GAE_DOMAIN/join for those respective actions.
SSL_LOGIN_ENABLED = False

#
# Appearance / Theme
#

# The default theme to use
DEFAULT_THEME = 'trotz'



#
# Cookie
#



CACHE_EXPIRES = 360000
#
# Blog
#

# Do you want /blog to redirect to your blog?
BLOG_ENABLED = False

# Where is your blog?
BLOG_URL = 'http://blog.onarena.com'
BLOG_FEED_URL = 'http://blog.onarena.com/feeds'


#
# API
#

# Setting this to True will make the public API accept all requests as being
# from ROOT with no regard to actual authentication.
# Never this set to True on a production site.
API_DISABLE_VERIFICATION = False

# These next three determine which OAuth Signature Methods to allow.
API_ALLOW_RSA_SHA1 = True
API_ALLOW_HMAC_SHA1 = True
API_ALLOW_PLAINTEXT = False

# These three determine whether the ROOT use should be allowed to use these
# methods, if any at all. Setting all of these to False will disable the
# ROOT user from accessing the public API
API_ALLOW_ROOT_RSA_SHA1 = True
API_ALLOW_ROOT_HMAC_SHA1 = True
API_ALLOW_ROOT_PLAINTEXT = False

# OAuth consumer key and secret values
ROOT_TOKEN_KEY = 'ROOT_TOKEN_KEY'
ROOT_TOKEN_SECRET = 'ROOT_TOKEN_SECRET'
ROOT_CONSUMER_KEY = 'ROOT_CONSUMER_KEY'
ROOT_CONSUMER_SECRET = 'ROOT_CONSUMER_SECRET'

# Allow support for legacy API authentication
API_ALLOW_LEGACY_AUTH = False
LEGACY_SECRET_KEY = 'I AM ALSO SECRET'




#
# Task Queue
#

# Enabling the queue will allow you to process posts with larger numbers
# of followers but will require you to set up a cron job that will continuously
# ping a special url to make sure the queue gets processed
QUEUE_ENABLED = True

# The secret to use for your cron job that processes your queue
QUEUE_VENDOR_SECRET = 'SECRET'


#
# Throttling Config
#

# This will control the max number of SMS to send over a 30-day period
THROTTLE_SMS_GLOBAL_MONTH = 10000




# Settings for remote services
IMAGE_UPLOAD_ENABLED = False
IMAGE_UPLOAD_URL = 'upload.example.com'

# Settings for Google Contacts import
GOOGLE_CONTACTS_IMPORT_ENABLED = False



FEEDS_ENABLED = False
MARK_AS_SPAM_ENABLED = True
PRESS_ENABLED = False
BADGES_ENABLED = True
HIDE_COMMENTS_ENABLED = True
MULTIADMIN_ENABLED = False
PRIVATE_CHANNELS_ENABLED = False
MARKDOWN_ENABLED = False
# Lists nicks of users participating in conversations underneath comment
# areas for posts. Clicking list items inserts @nicks into comment box.
# The list shows a maximum of 25 nicks.
COMMENT_QUICKLINKS_ENABLED = True
# If enabled, adds support for using access keys 1-9 to insert @nicks into
# comment box. Requires COMMENT_QUICKLINKS_ENABLED.
COMMENT_QUICKLINKS_ACCESSKEYS_ENABLED = False

PROFILE_DB = False

# Limit of avatar photo size in kilobytes
MAX_AVATAR_PHOTO_KB = 200

MAX_ACTIVATIONS = 10

# Email Test mode
EMAIL_TEST_ONLY = False

# Allowed email addresses for testing
EMAIL_TEST_ADDRESSES = []

# Email limiting, if this is set it will restrict users to those with
# email addresses in this domain
EMAIL_LIMIT_DOMAIN = None

# Things to measure to taste
MAX_COMMENT_LENGTH = 2000


# only use the memory file uploader, do not use the file system - not able to do so on
# google app engine
FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.MemoryFileUploadHandler',)
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 # the django default: 2.5MB


# Gdata Stuff
GDATA_CONSUMER_KEY = ''
GDATA_CONSUMER_SECRET = ''

def default_email_sender():
    try:
        return os.environ['DJANGO_DEFAULT_FROM_EMAIL']
    except KeyError:
        return 'termie@google.com'

DEFAULT_FROM_EMAIL = default_email_sender()
DEFAULT_UNITTEST_TO_EMAIL = 'unittests@example.com'

PROFILING_DATA_PATH = 'profiling/prof_db.csv'

GOOGLE_BUCKET = "https://storage.googleapis.com/onarena/"

STORAGE_URL  = "https://storage.googleapis.com/onarena"


SPORT_EVENTS = {
    'Soccer':       _("Soccer"),
    'Basketball':   _("Basketball"),
    'Volleyball':   _("Volleyball"),
    'Hockey':       _("Hockey"),            
    
    'Win':          _("Win"),
    'Lose':         _("Lose"),  
    'Draw':         _("Draw"),       
    'Drew':         _("Drew"),                     
                
    "Goal":         [_("Goal"),        "https://storage.googleapis.com/onarena/images/soccer_ball.png"],
    "Yellow Card":  [_("Yellow Card"), "https://storage.googleapis.com/onarena/images/yellow_card.png"],
    "Red Card":     [_("Red Card"),    "https://storage.googleapis.com/onarena/images/red_card.png"],
    "Penalty":      [_("Penalty"),     "" ],
    "Auto Goal":    [_("Auto Goal"),""],
    "Substitution": [_("Substitution"),""],
    "5th foal":     [_("5th foal"),""],
    }


POSITIONS = {
    'Forward' :     _("Forward"),
    'Defender':     _("Defender"),
    'Midfielder':   _("Midfielder"),
    'Goalkeeper':   _("Goalkeeper"),
    }        





ROOT_NICK = 'nik@onarena.com'
DEFAULT_FROM_EMAIL = 'mail@onarena.com'

SITE_NAME = 'OnArena.com'

#DEBUG = True
#TEMPLATE_DEBUG = True
ROOT_NICK = 'nik@onarena.com'

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')

VKONTAKE_ID = "4163414"#"2230899"#
FB_ADMIN = "645007811"

GOOGLE_SIMPLE_API = "AIzaSyAEqOgNFyVts9nrEZb5QVEDROnBTOVbjoY"




if DEBUG == True:
    TEMPLATE_DEBUG = True
    GAE_DOMAIN = 'http://178.49.10.142:8080'
    DOMAIN = 'http://178.49.10.142:8080'    
    NS_DOMAIN = 'http://178.49.10.142:8080'        
    
    GOOGLE_API_LIBRARY_KEY = "ABQIAAAA6V5m0H_1qIJiSfhkjsiGQRS66ZEasMyYFmrkiPGItVy1zQauPBSM92QHQxQeDGHCkDiNodbSNsrqxA"
    GOOGLE_CUSTOM_SEARCH = "partner-pub-7418245016943302:7ol7h4dczh1"    
    
    WILDCARD_USER_SUBDOMAINS_ENABLED = False
    SUBDOMAINS_ENABLED = False
    SSL_LOGIN_ENABLED = True
    
    
    FACEBOOK_API_KEY = "186848441325792"
    FACEBOOK_SECRET_KEY = "8a8531ebfb623b4aeb4e258802a0c04b"    

    MAIL_RU_ID = "600824"
    MAIL_RU_API_KEY = "0fcebbf9455e10f5e8f330faca9f5be4"
    MAIL_RU_SECRET_KEY = "262e3812d234a46d50080b6ab1f7aabe"

else:
    TEMPLATE_DEBUG = False
    GAE_DOMAIN = 'http://cometiphrd.appspot.com'
    DOMAIN = 'http://www.onarena.com'
    NS_DOMAIN = 'http://onarena.com' 
    
    GOOGLE_API_LIBRARY_KEY = "ABQIAAAA6V5m0H_1qIJiSfhkjsiGQRQq6RlFcGwqecaWjBDwiDNiJPGnRhS09KBACCCpP6-wR7tZqC28L8btvw"
    GOOGLE_CUSTOM_SEARCH = "005530471691595832073:zei0czo063m"    
    
    DEFAULT_FROM_EMAIL = 'mail@onarena.com'
    HOSTED_DOMAIN_ENABLED = True
    SECRET_KEY = 'f6578115c3e535f993da4a5858dc00d9'
    SSL_LOGIN_ENABLED = False
    HOSTED_DOMAIN = 'http://onarena.com'
            
    FACEBOOK_API_KEY = "127142214017014"
    FACEBOOK_SECRET_KEY = "53894a693c9badc17c7063051322929c"
    

# Cookie settings, pretty self explanatory, you shouldn't need to touch these.
USER_COOKIE = 'user'
PASSWORD_COOKIE = 'password'
COOKIE_DOMAIN = '.%s' % DOMAIN
COOKIE_PATH = '/'    
