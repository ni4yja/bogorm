from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
SECRET_KEY = env("SECRET_KEY")
GDAL_LIBRARY_PATH = "/opt/homebrew/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/opt/homebrew/lib/libgeos_c.dylib"
