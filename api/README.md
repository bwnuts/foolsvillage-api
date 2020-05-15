# API

### Table of Contents

[[_TOC_]]

## Issue

### Get an issue

```
GET /api/issue/:issue_id
```

#### Parameters

| name     | type     | description                                                |
|----------|----------|------------------------------------------------------------|
| `fields` | `string` | Comma separated list of fields to return.<br/>Default: all |

Available fields:
- `id`
- `title`
- `description`
- `state`
- `date`
- `creator`
- `approver`
- `pollution_category`
- `pollution_rating`
- `budget`
- `comments` - number of comments

#### Response

```
Status: 200 OK
```

```json
{
  "id": 1,
  "title": "Beach trash",
  "description": "helpful description",
  "state": "new",
  "date": "2000-01-01",
  "creator": {
    "id": 1,
    "username": "username",
    "role": "admin",
    "email": "example@gmail.com",
    "name": "John",
    "surname": "Doe",
    "gender": "male",
    "birthday": "2000-01-01",
    "phonenumber": "+11111111",
    "avatar": "<url>"
  },
  "approver": null,
  "pollution_category": "trash",
  "pollution_rating": 3.8,
  "budget": null,
  "comments": 12
}
```

### Get issue comments

```
GET /api/issue/:issue_id/comments
```

#### Parameters


| name     | type     | description                                                           |
|----------|----------|-----------------------------------------------------------------------|
| `offset` | `int`    | Comments to skip.                                                     |
| `count`  | `int`    | The maximum number of comments to return.<br>Default: 25, Maximum: 25 |
| `fields` | `string` | Comma separated list of fields to return.<br>Default: all             |

Available fields:
- `id`
- `text`
- `date`
- `author`
- `origin`

#### Response

```
Status: 200 OK
```

```json
[
  {
    "id": 1,
    "text": "Beach trash",
    "date": "2000-01-01",
    "author": {
      "id": 1,
      "username": "username",
      "role": "admin",
      "email": "example@gmail.com",
      "name": "John",
      "surname": "Doe",
      "gender": "male",
      "birthday": "2000-01-01",
      "phonenumber": "+11111111",
      "avatar": "<url>"
    },
    "origin": {
      "id": 1,
      "title": "Beach trash",
      "description": "helpful description",
      "state": "new",
      "date": "2000-01-01",
      "pollution_category": "trash",
      "pollution_rating": 3.8,
      "budget": null,
      "comments": 2
    }
  },
  {
    "id": 2,
    "text": "Beach trash trash",
    "date": "2000-01-01",
    "author": {
      "id": 1,
      "username": "username",
      "role": "admin",
      "email": "example@gmail.com",
      "name": "John",
      "surname": "Doe",
      "gender": "male",
      "birthday": "2000-01-01",
      "phonenumber": "+11111111",
      "avatar": "<url>"
    },
    "origin": {
      "id": 1,
      "title": "Beach trash",
      "description": "helpful description",
      "state": "new",
      "date": "2000-01-01",
      "pollution_category": "trash",
      "pollution_rating": 3.8,
      "budget": null,
      "comments": 2
    }
  }
]
```

## Event

### Get an event

```
GET /api/event/:event_id
```

#### Parameters

| name     | type     | description                                               |
|----------|----------|-----------------------------------------------------------|
| `fields` | `string` | Comma separated list of fields to return.<br>Default: all |

Available fields:
- `id`
- `issue`
- `creator`
- `datetime`
- `comments`  - number of comments
- `participants` - number of event participants

#### Response

```
Status: 200 OK
```

```json
{
  "id": 1,
  "issue": {
    "id": 1,
    "title": "Beach trash",
    "description": "helpful description",
    "state": "new",
    "date": "2000-01-01",
    "pollution_category": "trash",
    "pollution_rating": 3.8,
    "budget": null,
    "comments": 12
  },
  "creator": {
    "id": 1,
    "username": "username",
    "role": "admin",
    "email": "example@gmail.com",
    "name": "John",
    "surname": "Doe",
    "gender": "male",
    "birthday": "2000-01-01",
    "phonenumber": "+11111111",
    "avatar": "<url>"
  },
  "datetime": "2020-05-04 22:54:47.255134",
  "comments": 2,
  "participants": 0
}
```

### Get event comments

```
GET /api/event/:event_id/comments
```

#### Parameters


| name     | type     | description                                                            |
|----------|----------|------------------------------------------------------------------------|
| `offset` | `int`    | Comments to skip.                                                      |
| `count`  | `int`    | The maximum number of comments to return.<br> Default: 25, Maximum: 25 |
| `fields` | `string` | Comma separated list of fields to return.<br>Default: all              |

Available fields:
- `id`
- `text`
- `datetime`
- `author`
- `origin`

#### Response

```
Status: 200 OK
```

```json
[
  {
    "id": 1,
    "text": "Beach trash",
    "datetime": "2020-05-04 22:54:47.255134",
    "author": {
      "id": 1,
      "username": "username",
      "role": "admin",
      "email": "example@gmail.com",
      "name": "John",
      "surname": "Doe",
      "gender": "male",
      "birthday": "2000-01-01",
      "phonenumber": "+11111111",
      "avatar": "<url>"
    },
    "origin": {
      "id": 1,
      "datetime": "2020-05-04 22:54:47.255134",
      "comments": 2,
      "participants": 2
    }
  },
  {
    "id": 2,
    "text": "Beach trash trash",
    "datetime": "2020-05-04 22:54:47.255134",
    "author": {
      "id": 1,
      "username": "username",
      "role": "admin",
      "email": "example@gmail.com",
      "name": "John",
      "surname": "Doe",
      "gender": "male",
      "birthday": "2000-01-01",
      "phonenumber": "+11111111",
      "avatar": "<url>"
    },
    "origin": {
      "id": 1,
      "datetime": "2020-05-04 22:54:47.255134",
      "comments": 2,
      "participants": 2
    }
  }
]
```
