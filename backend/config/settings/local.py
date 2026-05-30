from ctypes.util import find_library

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
SECRET_KEY = env("SECRET_KEY")
# Resolve GIS libraries inside the active runtime (e.g., Docker Linux image).
# Env vars can still override these when a specific path is required.
GDAL_LIBRARY_PATH = env("GDAL_LIBRARY_PATH", default=find_library("gdal"))
GEOS_LIBRARY_PATH = env("GEOS_LIBRARY_PATH", default=find_library("geos_c"))
