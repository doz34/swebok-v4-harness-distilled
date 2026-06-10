Example
110
: Flattened form for included blocks
Open in playground

```
  [{
    "@id": "http://example.org/org-1",
    "http://example.org/members": [
      {"@id": "http://example.org/person-1"},
      {"@id": "http://example.org/person-2"},
      {"@id": "http://example.org/person-3"}
    ]
  }, {
    "@id": "http://example.org/employee",
    "http://example.org/label": [{"@value": "An Employee"}]
  }, {
    "@id": "http://example.org/contractor",
    "http://example.org/label": [{"@value": "A Contractor"}]
  }, {
    "@id": "http://example.org/person-1",
    "http://example.org/name": [{"@value": "Manu Sporny"}],
    "http://example.org/classification": [
      {"@id": "http://example.org/employee"}
    ]
  }, {
    "@id": "http://example.org/person-2",
    "http://example.org/name": [{"@value": "Dave Longley"}],
    "http://example.org/classification": [
      {"@id": "http://example.org/employee"}
    ]
  }, {
    "@id": "http://example.org/person-3",
    "http://example.org/name": [{"@value": "Gregg Kellogg"}],
    "http://example.org/classification": [
      {"@id": "http://example.org/contractor"}
    ]
  }
]
```
| Subject                           | Property                          | Value                             |
| --------------------------------- | --------------------------------- | --------------------------------- |
| http://example.org/org-1          | http://example.org/members        | http://example.org/person-1       |
| http://example.org/org-1          | http://example.org/members        | http://example.org/person-2       |
| http://example.org/org-1          | http://example.org/members        | http://example.org/person-3       |
| http://example.org/employee       | http://example.org/label          | An Employee                       |
| http://example.org/contractor     | http://example.org/label          | A Contractor                      |
| http://example.org/person-1       | http://example.org/name           | Manu Sporny                       |
| http://example.org/person-1       | http://example.org/classification | http://example.org/employee       |
| http://example.org/person-2       | http://example.org/name           | Dave Longley                      |
| http://example.org/person-2       | http://example.org/classification | http://example.org/employee       |
| http://example.org/person-3       | http://example.org/name           | Gregg Kellogg                     |
| http://example.org/person-3       | http://example.org/classification | http://example.org/contractor     |

```
@prefix ex: <http://example.org/> .

ex:org-1 ex:members ex:person-3,
    ex:person-1,
    ex:person-2 .

ex:person-1 ex:classification ex:employee;
  ex:name "Manu Sporny" .

ex:person-2 ex:classification ex:employee;
  ex:name "Dave Longley" .

ex:person-3 ex:classification ex:contractor;
  ex:name "Gregg Kellogg" .

ex:employee ex:label "An Employee" .
ex:contractor ex:label "A Contractor" .
```