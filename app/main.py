from fastapi import FastAPI, HTTPException
from app.schemas.item_schemas import ItemCreateUnion, ItemUpdate
from app.schemas.customer_schema import CustomerCreate
from app.services.item_factory import build_item_from_schema
from app.services.customer_factory import build_customer
from app.services.library_service import (
	add_item,
	get_all_items,
	get_single_item_service,
	delete_item_service,
	patch_item_service,
	add_customer,
	get_all_customers,
	get_customer_by_id,
	delete_customer,
	loan_item_service,
	return_item_service,
	get_loans
)

app = FastAPI()

@app.post("/items")
def create_item(data: ItemCreateUnion):
	item = build_item_from_schema(data)
	return add_item(item)

@app.get("/items")
def get_items():
	return get_all_items()

@app.get("/items/{item_id}")
def get_single_item(item_id: str):
	try:
		return get_single_item_service(item_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.delete("/items/{item_id}")
def del_item(item_id: str):
	try:
		return delete_item_service(item_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.put("/items/{item_id}")
def patch_item(item_id: str, update: ItemUpdate):
	try:
		return patch_item_service(item_id, update)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.post("/customers")
def create_customer(data: CustomerCreate):
	customer = build_customer(data)
	return add_customer(customer)

@app.get("/customers")
def get_customers():
	return get_all_customers()

@app.get("/customers/{customer_id}")
def get_single_customer(customer_id: str):
	try:
		return get_customer_by_id(customer_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.delete("/customers/{customer_id}")
def del_customer(customer_id: str):
	try:
		return delete_customer(customer_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.patch("/items/{item_id}")
def loan_item(item_id: str, customer_id: str):
	try:
		loan_item_service(item_id, customer_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.patch("/loans/{item_id}")
def return_item(item_id: str, customer_id: str):
	try:
		return return_item_service(item_id, customer_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.get("/loans")
def get_loan_pairs():
	return get_loans()