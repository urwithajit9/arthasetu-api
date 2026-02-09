INSTALLED_APPS = [
    ...
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Put this at the top
    ...
]

CORS_ALLOW_ALL_ORIGINS = True # For development