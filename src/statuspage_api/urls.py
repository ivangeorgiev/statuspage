from django.urls import path
from .views import (
  get_system_issue_counts,
  get_status_page,
  view_status_page,
  get_status_page1,
)

app_name = 'statuspage_api'

urlpatterns = [
  path('system/<str:nickname>/issues/counts/', get_system_issue_counts, name='get-system-status'),
  path('statuspage/<str:id>/', get_status_page, name='get-status-page'),
  path('view/statuspage/<str:id>/', view_status_page, name='view-status-page'),
  path('statuspage1/<str:id>/', get_status_page1, name='get_status_page1'),
]
