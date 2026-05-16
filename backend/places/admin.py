from django.contrib import admin  # pyright: ignore[reportMissingModuleSource]

from .models import Place

admin.site.register(Place)