import app.repositories.customer_repo as customer_repo
import app.repositories.items_repo as items_repo
import app.repositories.loans_repo as loan_repo
from app.mappers.customer_mapper import row_to_customer
from app.mappers.item_mapper import _row_to_item
from app.schemas.item_schemas import ItemUpdate


#ITEMS
def add_item(item):
	if item.price < 0:
		raise ValueError("Invalid price")

	items_repo.save_item(item)
	return item

def get_all_items():
	rows = items_repo.load_items()
	if not rows:
		return []

	return [
		_row_to_item(row)
		for row in rows
		if row is not None
	]

def get_single_item_service(item_id: str):
	item = items_repo.load_single_item(item_id)
	if not item:
		raise ValueError("Invalid Item-ID")
	return _row_to_item(item)

def delete_item_service(item_id: str):
	rows = items_repo.delete_item(item_id)

	if rows == 0:
		raise ValueError("Invalid Item-ID")

	return True

def patch_item_service(item_id: str, update: ItemUpdate):
	data = update.model_dump(exclude_unset=True, exclude_none=True)

	if not data:
		raise ValueError("Invalid Update Type")

	rows = items_repo.update_item(item_id, data)

	if rows == 0:
		raise ValueError("Invalid Item-ID")

	item = items_repo.load_single_item(item_id)
	return _row_to_item(item)


#CUSTOMERS
def get_customer_by_id(customer_id: str):
	row = customer_repo.load_customer_by_id(customer_id)

	if not row:
		raise ValueError("Customer not found")

	return row_to_customer(row)

def get_all_customers():
	rows = customer_repo.load_customers()
	return [row_to_customer(r) for r in rows]

def add_customer(customer):
	customer_repo.save_customer(customer)
	return get_customer_by_id(customer.id)

def delete_customer(customer_id: str):
	row = customer_repo.load_customer_by_id(customer_id)
	if not row:
		raise ValueError("Customer not found")
	customer = row_to_customer(row)
	if customer.borrowed > customer.returned:
		raise ValueError("Items need to be returned")
	return customer_repo.del_customer(customer.id)

#LOANS
def loan_item_service(item_id: str, customer_id: str):
	row = customer_repo.load_customer_by_id(customer_id)
	customer = row_to_customer(row)
	i = items_repo.load_single_item(item_id)
	item = _row_to_item(i)

	if not customer or not item:
		raise ValueError("Invalid ID")

	if item.on_loan:
		raise ValueError("Item already loaned")

	new_count = customer.borrowed + 1

	if new_count > customer.returned + 3:
		raise ValueError("Limit reached")

	customer.borrowed = new_count

	items_repo.update_loan_status(item_id, True)
	customer_repo.update_borrowed_count(customer.id, new_count)
	loan_repo.save_loan_pair(item_id, customer.id)

	return item

def return_item_service(item_id: str, customer_id):
	row = items_repo.load_single_item(item_id)
	item = _row_to_item(row)
	i = customer_repo.load_customer_by_id(customer_id)
	customer = row_to_customer(i)

	if not item:
		raise ValueError("Item not found")
	if not item.on_loan:
		raise ValueError("Item not on loan")
	loan_pair = loan_repo.get_loan_pair(item_id, customer_id)
	if not loan_pair:
		raise ValueError("Loan Pair not found")

	items_repo.update_loan_status(item_id, False)
	new_count = customer.returned + 1
	customer_repo.update_returned_count(customer_id, new_count)
	loan_repo.delete_loan_pair(item_id, customer_id)

	return True


def get_loans():
	return loan_repo.load_loan_pairs()