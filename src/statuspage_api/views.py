from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import System, Issue, StatusPage
from collections import defaultdict
from django.db.models import Count, F
import json

def make_error_response(response_constructor, error_code, message):
  data = {
    'error': error_code,
    'message': message,
  }
  return response_constructor(json.dumps(data), content_type='application/json')

def get_system_issue_counts(request, nickname:str):
  qs = System.objects.filter(nickname=nickname)
  if not qs:
    return HttpResponseNotFound("Not found")
  system = qs[0]
  issues = Issue.objects.all().filter(system_id__exact=system.system_id, 
      is_resolved__exact=False)
  tag_counts = issues.values(severity=F('tags__severity'), name=F('tags__name')).annotate(count=Count('severity'))
  s = {
    'name': qs[0].name,
    'open_issues': {
      'count': issues.count(),
      'by_severity': {t['severity']:{'count':t['count'], 'label':t['name']} for t in tag_counts}
    }
  }

  return JsonResponse(s)

def get_status_page(request, id):
  try:
    status_page = StatusPage.objects.get(status_page_id=id)
  except StatusPage.DoesNotExist as exc:
    return make_error_response(HttpResponseNotFound, 'ERR_NOT_FOUND', f"Status page '{id}' not found")

  response = {
    'name': status_page.name,
    'id': status_page.status_page_id,
    'categories': []
  }

  categories = status_page.categories.all()

  for category in categories:
    systems = []
    for system in category.systems.order_by('rank').all():
      issues = Issue.objects.all().filter(system_id__exact=system.system_id, 
          is_resolved=False)
      tag_counts = issues.values(severity=F('tags__severity'), name=F('tags__name')).annotate(count=Count('severity'))
      system_record = {
        'id': system.system_id,
        'name': system.name,
        'description': system.description,
        'rank': system.rank,
        'open_issues': {
          'count': issues.count(),
          'by_severity': {t['severity']:{'count':t['count'], 'label':t['name']} for t in tag_counts}
        }
      }
      systems.append(system_record)

    
    category_record = {
      'id': category.system_category_id,
      'name': category.name,
      'rank': category.rank,
      'systems': systems,
    }
    
    response['categories'].append(category_record)

  return JsonResponse(response)


def view_status_page(request, id):
  context = {
    'url_get_status_page': f'/api/statuspage1/{id}/',
    'auto_refresh_interval': 300000,
  }
  return render(request, 'api/status_page.html', context)


def get_status_page1(request, id):
  def get_system_record(system):
    issues = system.issues.all()
    open_issues = issues.filter(is_resolved=False)
    tag_counts = open_issues.values(severity=F('tags__severity'), name=F('tags__name')).annotate(count=Count('severity'))
    subsystem_tag_counts = defaultdict(lambda : {'count':0, 'label': ''})
    for c in tag_counts:
      subsystem_tag_counts[c['severity']] = {
        'count': c['count'],
        'label': c['name'],
        }
    subsystem_issue_count = 0
    for subsystem in system.subsystems.all():
      sysbsystem_record = get_system_record(subsystem)
      for severity, item in sysbsystem_record['open_issues']['by_severity'].items():
        count = item['count']
        subsystem_tag_counts[severity]['count'] += count
        subsystem_tag_counts[severity]['label'] = item['label']
        subsystem_issue_count += count
    system_record = {
      'id': system.system_id,
      'parent_id': system.parent_system.system_id if system.parent_system else None,
      'name': system.name,
      'description': system.description,
      'open_issues': {
        'count': open_issues.count(),
        'by_severity': {t['severity']:{'count':t['count'], 'label':t['name']} for t in tag_counts},
        'with_subsystems': {
          'count': subsystem_issue_count,
          'by_severity': subsystem_tag_counts,
        }
      }
    }
    return system_record


  try:
    status_page = StatusPage.objects.get(status_page_id=id)
  except StatusPage.DoesNotExist as exc:
    return make_error_response(HttpResponseNotFound, 'ERR_NOT_FOUND', f"Status page '{id}' not found")

  response = {
    'id': status_page.status_page_id,
    'name': status_page.name,
    'description': status_page.description,
    'systems': []
  }

  systems = status_page.systems.all()
  for system in systems:
    system_record = get_system_record(system)
    response['systems'].append(system_record)
  return JsonResponse(response)
