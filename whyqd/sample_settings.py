"""
Whyqd uses a fair number of APIs and this sample settings file will give
you the basic requirements you'll need.

Note: this is definitely NOT a full settings file, so use it to add to your
project settings.py

API Keys include:
    - OpenExchangeRates (OXR) (https://openexchangerates.org/)
    - Stripe (https://stripe.com/)
    - AWS S3 (http://aws.amazon.com/)
    - Mandrill (https://mandrill.com/)
    
Additional Django libraries have their own requirements:
    - Django-Facebook (https://github.com/tschellenbach/Django-facebook)
    - Guardian (https://github.com/lukaszb/django-guardian)
    - Mathfilters (https://github.com/dbrgn/django-mathfilters)
    - Djrill (Django Mandrill) (https://github.com/brack3t/Djrill/)
    - Widget-tweaks (https://github.com/kmike/django-widget-tweaks)
"""

# Caching required to store OXR rates
# https://docs.djangoproject.com/en/1.7/topics/cache/
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "", # Give it a unique name
        "TIMEOUT": 60 * 60 * 8 # Make it eight hours since it's a slow-changing site
    }
}

INSTALLED_APPS = (
    # Whyqd-specific libraries included:
    # External Libraries
    "guardian",
    "django_facebook",
    "mathfilters",
    "djrill",
    "widget_tweaks",
    # Whyqd Apps
    "whyqd.wiqi",
    "whyqd.usr",
    "whyqd.novel",
)

AUTH_USER_MODEL = "usr.User"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

# UUID initialisation for surls (short-urls)
SURL_ALPHABET = "" # Set your own alphabet here for use as a random key
SURL_LENGTH = 12
TOKEN_SURL_LENGTH = 22 # Longer surl for greater security

# Settings for Novels and Tokens
TOKEN_DELTA = 30 # Number of days book loaned out
TOKEN_LIMIT = 5
BULK_DISCOUNT = 0.2 #20% discount
BULK_VOLUME = 5 #5 minimum order to get BULK_DISCOUNT
BULK_PRICE = 2.99 #Starter price
DEFAULT_PRICE = 299 #Stripe requires cents/pence
DEFAULT_CURRENCY = "GBP"

# Django Guardian Setting
ANONYMOUS_USER_ID = -1

# Auth and Django_Facebook settings
LOGIN_REDIRECT_URL = "/"
FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""
FACEBOOK_DEFAULT_SCOPE = ["email"]

# Stripe API Keys (remember to swap when in production)
TEST_SECRET_KEY = ""
TEST_PUBLISHABLE_KEY = ""
LIVE_SECRET_KEY = ""
LIVE_PUBLISHABLE_KEY = ""
STRIPE_SECRET_KEY = TEST_SECRET_KEY
STRIPE_PUBLISHABLE_KEY = TEST_PUBLISHABLE_KEY

# Openexchangerates.org API key
OPEXRATE_API_KEY = ""
OPEXRATE_API_URL = ""

# AWS S3 and SES Keys for Boto
S3_USER_NAME = ""
S3_ACCESS_KEY_ID = ""
S3_SECRET_ACCESS_KEY = ""
S3_EBOOK_BUCKET = ""
S3_EBOOK_DOWNLOAD_FOLDER = ""
S3_TIMER = 60

# Djrill settings for Mandrill Emailer
MANDRILL_API_KEY = ""
MANDRILL_SUBACCOUNT = ""
EMAIL_FROM_ADDR = ""