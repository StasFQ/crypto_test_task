### 1. Create wallet

Create a new wallet for user.

```http
POST http://127.0.0.1:5050/generate_wallets
```


#### Parameters

| Name	         | Type  | 	Required | 	Description                                 |
|---------------|-------|-----------|----------------------------------------------|
    -               -           -           -

#### Headers

Authorization: Access token

#### Example

- Request:



- Response:

```json
{
  "message": "Wallet created successfully"
}
```

### 2. Make a transaction

Make a transaction.

```http
POST http://127.0.0.1:5050/transaction
```


#### Parameters

| Name     | Type | Required | Values(default) | Description |
|----------|------|----------|-----------------|-------------|
| recipient_address | str  | Yes      | None            | To address  |
 | amount_eth | int | Yes | None | amount of eth to send |

#### Headers

Authorization: Access token

#### Example

- Request:
```json
{
    "recipient_address": "0xEE046045454E9012AB1bCE9496d54D3680477b17",
    "amount_eth": 0.2

}
```


- Response:

```json
{
  "message": "Transaction sent successfully."
}
```

### 3. Get a transaction

Get a transaction.

```http
GET http://127.0.0.1:5050/transactions/get
```


#### Parameters

| Name     | Type | Required | Values(default) | Description   |
|----------|------|----------|-----------------|---------------|
| currency | str  | No       | None            | Crypto        |
 | amount | int | No       | None | amount of eth |
 | tx_hash | str  | No       | None            | hash          |
 | page | int | No       | None | pagination    |
 | per_page | int | No       | None | pagination    |

#### Headers

Authorization: Access token

#### Example

- Request:
```json
{
  "currency": "ETH",
  "amount": 100,
  "tx_hash": "0x123456789",
  "page": 1,
  "per_page": 10
}
```


- Response:

```json
{
 "transactions": [
  {
   "id": 1,
   "currency": "ETH",
   "amount": 100,
   "tx_hash": "0x123456789",
  },
  {
   "id": 2,
   "currency": "ETH",
   "amount": 100,
   "tx_hash": "0x987654321",
  }
 ]
}
```

