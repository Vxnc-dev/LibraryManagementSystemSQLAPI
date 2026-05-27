from fastapi import FastAPI, HTTPException, status
from app.schemas.item_schemas import ItemCreateUnion, ItemUpdate
from app.schemas.customer_schema import CustomerCreate
from app.services.item_factory import build_item_from_schema
from app.services.customer_factory import build_customer
import app.services.library_service as lib

app = FastAPI()

@app.post("/items")
def create_item(data: ItemCreateUnion):
	try:
		item = build_item_from_schema(data)
		return lib.add_item(item)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))

@app.get("/items")
def get_items():
	return lib.get_all_items()

@app.get("/items/{item_id}")
def get_single_item(item_id: str):
	try:
		return lib.get_single_item_service(item_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def del_item(item_id: str):
	try:
		lib.delete_item_service(item_id)
		return
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.put("/items/{item_id}")
def patch_item(item_id: str, update: ItemUpdate):
	try:
		return lib.patch_item_service(item_id, update)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/customers")
def create_customer(data: CustomerCreate):
	customer = build_customer(data)
	return lib.add_customer(customer)

@app.get("/customers")
def get_customers():
	return lib.get_all_customers()

@app.get("/customers/{customer_id}")
def get_single_customer(customer_id: str):
	try:
		return lib.get_customer_by_id(customer_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.delete("/customers/{customer_id}")
def del_customer(customer_id: str):
	try:
		return lib.delete_customer(customer_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.patch("/items/{item_id}")
def loan_item(item_id: str, customer_id: str):
	try:
		lib.loan_item_service(item_id, customer_id)
		return {"message": "loaned"}
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.patch("/loans/{item_id}")
def return_item(item_id: str, customer_id: str):
	try:
		return lib.return_item_service(item_id, customer_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

@app.get("/loans")
def get_loan_pairs():
	return lib.get_loans()