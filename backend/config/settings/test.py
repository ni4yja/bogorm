from .local import *

# Defaults to localhost; CI runs tests in a container and sets this to the
# service name ("postgres"), since localhost there is the container itself.
DATABASES["default"]["HOST"] = env("DATABASE_HOST", default="localhost")
