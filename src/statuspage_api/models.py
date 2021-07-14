from django.db import models
from datetime import datetime

ENUM_ISSUE_STATUS = (
  ('N', 'New'),
  ('I', 'Under Investigation'),
  ('R', 'Resolved'),
  ('C', 'Closed'),
)
RESOLVED_ISSUE_STATUSES = ['C', 'R']

ENUM_ISSUE_TAG_SEVERITY = (
  ('Outage', 'Major outage'),
  ('Degraded', 'Degraded performance'),
  ('Minor', 'Minor'),
)

class StatusPage(models.Model):
  status_page_id = models.CharField(max_length=255, primary_key=True)
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  systems = models.ManyToManyField('System', related_name='status_papges', blank=True)

  class Meta:
    ordering = ('name',)
 
  def __str__(self):
    return f'{self.name}'

class SystemCategory(models.Model):
  system_category_id = models.BigAutoField(primary_key=True)
  name = models.CharField(max_length=255)
  rank = models.IntegerField()
  status_page = models.ForeignKey(StatusPage, on_delete=models.CASCADE, related_name='categories', null=True)

  class Meta:
    ordering = ('status_page', 'rank', 'name',)
    verbose_name_plural = 'system categories'

  def __str__(self):
    groups = self.groups.all()
    groups_str = ', '.join([f'{g.system_group_id}: {g.name}' for g in groups])
    return f'{self.rank}. {self.name} [{self.system_category_id}] - [{groups_str}]'

class SystemGroup(models.Model):
  system_group_id = models.BigAutoField(primary_key=True)
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  categories = models.ManyToManyField(SystemCategory, related_name='groups')
  rank = models.IntegerField(default=0)

  class Meta:
    ordering = ('rank', 'name', 'system_group_id',)

  def __str__(self):
    systems = self.systems.all()
    systems_str = ', '.join([f'{s.system_id}: {s.name}' for s in systems])
    return f'{self.rank}. {self.name} [{self.system_group_id}] - [{systems_str}]'

class System(models.Model):
  system_id = models.CharField(max_length=255, primary_key=True)
  parent_system = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="subsystems")
  parent_system_id_path = models.CharField(max_length=2048, blank=True, null=True)
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  categories = models.ManyToManyField(SystemCategory, related_name='systems', blank=True)
  groups = models.ManyToManyField(SystemGroup, related_name='systems', blank=True)
  rank = models.IntegerField(default=0)

  class Meta:
    ordering = ('parent_system_id_path', 'rank', 'name', 'system_id', )
    indexes = [
      models.Index(fields=['system_id']),
      models.Index(fields=['parent_system_id_path']),
    ]

  def __str__(self):
    return f'{self.parent_system_id_path} - {self.name}'


class IssueTag(models.Model):
  tag_id = models.BigAutoField(primary_key=True)
  name = models.CharField(max_length=255)
  severity = models.CharField(max_length=64, choices=ENUM_ISSUE_TAG_SEVERITY, default='Outage')

  def __str__(self):
    return f'{self.name}'

class Issue(models.Model):
  issue_id = models.BigAutoField(primary_key=True)
  original_issue_id = models.CharField(max_length=255)
  system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='issues')
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  tags = models.ManyToManyField(IssueTag, blank=True, related_name='issues')
  status = models.CharField(max_length=64, choices=ENUM_ISSUE_STATUS, default='N')
  is_resolved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  resolved_at = models.DateTimeField(default=None, null=True, blank=True)

  class Meta:
    indexes = [
      models.Index(fields=['original_issue_id'])
    ]

  def __str__(self):
    return f'{self.issue_id}: {self.title}'
