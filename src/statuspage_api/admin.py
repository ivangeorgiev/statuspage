from django.contrib import admin

from .models import (
  Issue,
  IssueTag,
  StatusPage,
  System,
  SystemGroup,
  SystemCategory,
)

admin.site.register(Issue)
admin.site.register(IssueTag)
admin.site.register(StatusPage)
admin.site.register(System)
admin.site.register(SystemGroup)
admin.site.register(SystemCategory)
