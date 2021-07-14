from django.urls import path
from .views import (
  get_system_issue_counts,
  get_status_page,
  view_status_page,
  view_issue,
  view_system_issue,
)

app_name = 'statuspage_api'

urlpatterns = [
  path('system/<str:nickname>/issues/counts/', get_system_issue_counts, name='get-system-status'),
  path('issue/<int:id>/', view_issue, name='view-issue'),
  path('issue/<str:system_id>/<str:issue_id>/', view_system_issue, name='view-system-issue'),
  path('statuspage/<str:id>/', get_status_page, name='get-status-page'),
  path('view/statuspage/<str:id>/', view_status_page, name='view-status-page'),
]
