# Media Library API

A REST API for managing a media library built with FastAPI and SQLite.

The project supports different media types such as books, films, comics, series, music, and games, including customer management and loan tracking.

---

## Features

### Items
- Create media items
	- Book
	- Film
	- Comic
	- Series
	- Music
	- Game

- View all items
- View single item by ID
- Update item data
- Delete items

### Customers
- Create customers
- View all customers
- View customer by ID
- Delete customers

### Loans
- Loan items to customers
- Return items
- Prevent duplicate loans
- Borrow limit per customer
	- max 3 active loans

---

## Tech Stack

- Python 3
- FastAPI
- SQLite
- Pydantic
- Uvicorn

---

## Project Structure

```bash
app/
│
├── main.py
│
├── mappers/
│   ├── customer_mapper.py
│   └── item_mapper.py
├── models/
│   ├── customer.py
│   └── item.py
├── repositories/
│   ├── customer_repo.py
│   ├── items_repo.py
|	└── loans_repo.py
├── schemas/
│   ├── customer_schema.py
│   └── item_schema.py
├── services/
│   ├── customer_factory.py
│   ├── item_factory.py
|	└── library_service.py
```

---

## Installation

Clone repository:

```bash
git clone <https://github.com/Vxnc-dev/LibraryManagementSystemSQLAPI.git>
cd media-library-api
```

Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

Run server:

```bash
uvicorn app.main:app --reload
```

Server runs on:

```bash
http://127.0.0.1:8000
```

Swagger docs:

```bash
http://127.0.0.1:8000/docs
```

---

## Example Requests

## Create Book

`POST /items`

```json
{
	"type": "Book",
	"title": "Clean Code",
	"price": 29.99,
	"author": "Robert C. Martin",
	"year": 2008
}
```

---

## Create Film

```json
{
	"type": "Film",
	"title": "Interstellar",
	"price": 19.99,
	"year": 2014
}
```

---

## Create Customer

`POST /customers`

```json
{
	"name": "Vinc"
}
```

---

## Loan Item

`PATCH /items/{item_id}?customer_id=C0001`

---

## Return Item

`PATCH /loans/{item_id}?customer_id=C0001`

---

## Delete Item

`DELETE /items/{item_id}`

---

## Business Rules

- An item cannot be loaned twice simultaneously
- A customer can borrow max 3 items at once
- Customers with active loans cannot be deleted
- Returning is only allowed if the correct customer-item loan pair exists

---

## Future Improvements

- Authentication
- Pagination
- Search/filter endpoints
- Docker support
- Unit tests
- Alembic migrations / SQLAlchemy

---

## Author

Built as a learning project for practicing:
- FastAPI
- layered architecture
- repositories/services/mappers
- SQLite integration
- API design
