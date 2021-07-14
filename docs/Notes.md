## GET /statuspage/\<str:id\>

Get status page details

Response:

```yaml
statuspage:
  id: sp-user
  name: Contoso Limited
  description: Contoso Limited IT systems status page
  systems:
    - id: sys-portal
      parent_id:
      name: Web Portal
      description: Contoso Web Portal
      open_issues:
        count: 123
        severity:
          - critical:
            count: 123
```





## Resources

- https://onlineyamltools.com/convert-yaml-to-json