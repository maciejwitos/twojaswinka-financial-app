# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'twoja.swinka.pl@gmail.com'
EMAIL_HOST_PASSWORD = 'Twoja$winka2020'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'Twoja Świnka twoja.swinka.pl@gmail.com'