Common
-----------

Common HTTP Status

| Code | Status | Description |
|------|--------|-------------|
| 400  | Bad Request | Server cannot or will not process the request |
| 404  | Not Found |  Resource Not Found |
| 500  | Internal Server Error | Server side issue occurred. Please contact administrator |


List all orders
-----------

GET /api/orders/

Sample Response

HTTP Status Code: 200 (OK)


``` json

  [
      {
        "uid": "92fa6266-4f03-475f-af10-25f67431207c",
        "customer": 10,
        "status": "delivered",
        "status_text": "Delivered",
        "address": "123 Main Street, New York, NY 10030"
      },
      {
        "uid": "0a99bc9d-5868-4911-82c5-b17eee2804d4",
        "customer": 9,
        "status": "cancelled",
        "status_text": "Cancelled",
        "address": "P.O. Box 283 8562 Fusce Rd."
      },
  ]

```

Create an order
-----------

POST /api/orders

Sample Request

``` json

  {
    "customer_id": 8,
    "customer_address": "John Doe 123 Main St Anytown, USA",
    "products": [
      {
        "pizza": 22,
        "quantity": 1,
        "size": 4
      },
      {
        "pizza": 23,
        "quantity": 2,
        "size": 1
      },
    ]
  }

 ```

Sample Response

HTTP Status Code: 201 (Accepted)

``` json

  {}

```

Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 400  | Bad Request |  There are one or more errors in request value |


Show an order
-----------

GET /api/orders/:uid/

Sample Response

HTTP Status Code: 200 (OK)

``` json

  {
    "status": "delivered",
    "status_text": "Delivered",
    "address": "P.O. Box 283 8562 Fusce Rd.",
    "customer": {
      "user_name": "s2ci.john",
      "full_name": "John Doe"
    }
  }
```

Update an order
-----------

PUT /api/orders/:uid

Sample Request

``` json

  {
    "products": [
      { 
        "pizza": 21,
        "quantity": 3,
        "size": 1
      },
      { 
        "pizza": 20,
        "quantity": 4,
        "size": 3
      },
    ]
  }

```

Sample Response

HTTP Status Code: 200 (OK)

``` json

  {}

```

Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 400  | Bad Request |  There are one or more errors in request value |
| 404  | Not Found | Resource not found. |



Delete an order
-----------

DELETE /api/orders/:uid

HTTP Status Code: 204 (No Content)

Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 404  | Not Found | Resource not found. |

