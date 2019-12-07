import os


class Config:
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    DEBUG = os.environ.get('DEBUG', True)
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = os.environ.get('PORT', 5000)

    HERE_MAPS_API_ID = os.environ.get('HERE_MAPS_APP_ID')
    HERE_MAPS_APP_KEY = os.environ.get('HERE_MAPS_APP_KEY')
