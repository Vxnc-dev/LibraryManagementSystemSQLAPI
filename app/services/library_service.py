from app.repositories.customer_repo import load_customers, load_customer_by_id, update_borrowed_count, update_returned_count, save_customer, del_customer
from app.repositories.items_repo import save_item, load_items, load_single_item, delete_item, update_item, update_loan_status
from app.repositories.loans_repo import save_loan_pair, load_loan_pairs, get_loan_pair, delete_loan_pair
from app.mappers.customer_mapper import row_to_customer
from app.mappers.item_mapper import _row_to_item
from app.schemas.item_schemas import ItemUpdate


#ITEMS
def add_item(item):
	if item.price < 0:
		raise ValueError("Invalid price")

	save_item(item)
	return item

def get_all_items():
	rows = load_items()
	if not rows:
		return []

	return [
		_row_to_item(row)
		for row in rows
		if row is not None
	]

def get_single_item_service(item_id: str):
	item = load_single_item(item_id)
	if not item:
		raise ValueError("Invalid Item-ID")
	return _row_to_item(item)

def delete_item_service(item_id: str):
	rows = delete_item(item_id)

	if rows == 0:
		raise ValueError("Invalid Item-ID")

	return True

def patch_item_service(item_id: str, update: ItemUpdate):
	data = update.model_dump(exclude_unset=True, exclude_none=True)
	if not data:
		raise ValueError("Invalid Update Type")
	rows = update_item(item_id, data)
	if rows == 0:
		raise ValueError("Invalid Item-ID")
	return {"message:" "updated"}


#CUSTOMERS
def get_customer_by_id(customer_id: str):
	row = load_customer_by_id(customer_id)

	if not row:
		raise ValueError("Customer not found")

	return row_to_customer(row)

def get_all_customers():
	rows = load_customers()
	return [row_to_customer(r) for r in rows]

def add_customer(customer):
	return save_customer(customer)

def delete_customer(customer_id: str):
	row = load_customer_by_id(customer_id)
	if not row:
		raise ValueError("Customer not found")
	customer = row_to_customer(row)
	if customer.borrowed > customer.returned:
		raise ValueError("Items need to be returned")
	return del_customer(customer.id)

#LOANS
def loan_item_service(item_id: str, customer_id: str):
	row = load_customer_by_id(customer_id)
	customer = row_to_customer(row)
	i = load_single_item(item_id)
	item = _row_to_item(i)

	if not customer or not item:
		raise ValueError("Invalid ID")

	if item.on_loan:
		raise ValueError("Item already loaned")

	new_count = customer.borrowed + 1

	if new_count > customer.returned + 3:
		raise ValueError("Limit reached")

	customer.borrowed = new_count

	update_loan_status(item_id, True)
	update_borrowed_count(customer.id, new_count)
	save_loan_pair(item_id, customer.id)

	return item

def return_item_service(item_id: str, customer_id):
	row = load_single_item(item_id)
	item = _row_to_item(row)
	i = load_customer_by_id(customer_id)
	customer = row_to_customer(i)

	if not item:
		raise ValueError("Item not found")
	if not item.on_loan:
		raise ValueError("Item not on loan")
	loan_pair = get_loan_pair(item_id, customer_id)
	if not loan_pair:
		raise ValueError("Loan Pair not found")

	update_loan_status(item_id, False)
	new_count = customer.returned + 1
	update_returned_count(customer_id, new_count)
	delete_loan_pair(item_id, customer_id)

	return True


def get_loans():
	return load_loan_pairs()