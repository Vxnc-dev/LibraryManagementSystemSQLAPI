from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_customers_structure():
	response = client.get("/customers")

	assert response.status_code == 200

	for customer in response.json():
		assert "name" in customer

def test_get_customers():
	response = client.get("/customers")

	assert response.status_code == 200

	data = response.json()

	assert isinstance(data, list)

def test_create_customer_invalid():
	response = client.post("/customers", json={})

	assert response.status_code in (400, 422)

def test_get_single_customer():
	create_res = client.post("/customers", json={
		"name": "Vinc"
	})

	customer_id = create_res.json()["id"]

	response = client.get(f"/customers/{customer_id}")

	assert response.status_code == 200

	data = response.json()
	assert data["name"] == "Vinc"

def test_get_single_customer_not_found():
	response = client.get("/customers/does-not-exist")

	assert response.status_code == 404
	assert "Customer not found" in response.json()["detail"]

def test_delete_customer():
	create_res = client.post("/customers", json={
		"name": "Vinc"
	})

	customer_id = create_res.json()["id"]

	response = client.delete(f"/customers/{customer_id}")

	assert response.status_code == 200
	assert response.json() is True or response.json() is None

def test_delete_customer_not_found():
	response = client.delete("/customers/invalid-id")

	assert response.status_code == 404
	assert "Customer not found" in response.json()["detail"]

def test_delete_customer_open_loan():
	# 1. create customer
	customer = client.post("/customers", json={
		"name": "Vinc"
	}).json()
	customer_id = customer["id"]

	# 2. create item
	item = client.post("/items", json={
		"type": "Book",
		"title": "Clean Code",
		"price": 29.99,
		"author": "Robert C. Martin",
		"year": 2008
	}).json()
	item_id = item["id"]

	# 3. loan item to customer
	loan_res = client.patch(
		f"/items/{item_id}",
		params={"customer_id": customer_id}
	)

	assert loan_res.status_code == 200

	# 4. try to delete customer
	delete_res = client.delete(f"/customers/{customer_id}")

	assert delete_res.status_code == 404
	assert "items need to be returned" in delete_res.json()["detail"].lower()

