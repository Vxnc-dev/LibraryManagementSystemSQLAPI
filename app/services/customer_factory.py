from app.models.customer import Customer


def build_customer(data):
	c = Customer(data.name)
	return c