### 1. Create a user

Create a  user.

```http
POST http://localhost:5050/register
```


#### Parameters

| Name     | Type | Required | Values(default) | Description |
|----------|------|----------|-----------------|-------------|
| email    | str  | Yes      | None            | email       |
 | password | str  | Yes | None | password    |

#### Headers

-

#### Example

- Request:
```json
{
    "email": "example@gmail.com",
    "password": "example"

}
```

- Response:

```json
{
  "message": "User registered successfully."
}
```
### 2. Login

Login.

```http
POST http://localhost:5050/login
```


#### Parameters

| Name     | Type | Required | Values(default) | Description |
|----------|------|----------|-----------------|-------------|
| email    | str  | Yes      | None            | email       |
 | password | str  | No       | None | password    |

#### Headers

-

#### Example

- Request:
```json
{
    "email": "example@gmail.com",
}
```

- Response:

```json
{
  "acces_token": "dfgsdf23f23fbh2efh2f2f2fcw"
}
```
