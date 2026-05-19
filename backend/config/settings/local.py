from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-$10cn5b7(xtn6a)#x-3(6n7o@$%ql5!ny32+^)0^^2=yyn0c7j",
)
