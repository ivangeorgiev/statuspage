from django.contrib import admin

from .models import (
  Issue,
  StatusPage,
  System,
)

admin.site.register(Issue)
admin.site.register(StatusPage)
admin.site.register(System)

