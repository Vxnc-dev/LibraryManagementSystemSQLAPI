from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_loan_cycle():
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

	# 3. loan item
	loan_res = client.patch(
		f"/items/{item_id}",
		params={"customer_id": customer_id}
	)

	assert loan_res.status_code == 200

	# 4. check item is on loan
	item_after_loan = client.get(f"/items/{item_id}").json()
	assert item_after_loan["on_loan"] is True

	# 5. return item
	return_res = client.patch(
		f"/loans/{item_id}",
		params={"customer_id": customer_id}
	)

	assert return_res.status_code == 200

	# 6. check item is available again
	item_after_return = client.get(f"/items/{item_id}").json()
	assert item_after_return["on_loan"] is False

def test_loan_item_already_loaned():
	# 1. create customer A
	customer_a = client.post("/customers", json={
		"name": "Alice"
	}).json()
	customer_a_id = customer_a["id"]

	# 2. create customer B
	customer_b = client.post("/customers", json={
		"name": "Bob"
	}).json()
	customer_b_id = customer_b["id"]

	# 3. create item
	item = client.post("/items", json={
		"type": "Book",
		"title": "Clean Code",
		"price": 29.99,
		"author": "Robert C. Martin",
		"year": 2008
	}).json()
	item_id = item["id"]

	# 4. customer A loans item
	res1 = client.patch(
		f"/items/{item_id}",
		params={"customer_id": customer_a_id}
	)

	assert res1.status_code == 200

	# 5. customer B tries to loan same item
	res2 = client.patch(
		f"/items/{item_id}",
		params={"customer_id": customer_b_id}
	)

	assert res2.status_code == 404
	assert "already loaned" in res2.json()["detail"].lower()