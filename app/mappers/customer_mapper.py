from app.models.customer import Customer

def row_to_customer(row):
	customer_id, name, borrowed, returned = row

	customer = Customer(name)
	customer.id = customer_id
	customer.borrowed = borrowed
	customer.returned = returned

	return customer
