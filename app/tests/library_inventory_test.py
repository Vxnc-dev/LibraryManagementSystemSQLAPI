from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
	payload = {
		"type": "Book",
		"title": "Clean Code",
		"price": 29.99,
		"author": "Robert C. Martin",
		"year": 2008
	}

	response = client.post("/items", json=payload)

	assert response.status_code == 200
	data = response.json()
	assert data["title"] == "Clean Code"

def test_create_item_invalid_price():
	payload = {
		"type": "Book",
		"title": "Clean Code",
		"price": -10,
		"author": "Robert C. Martin",
		"year": 2008
	}

	response = client.post("/items", json=payload)

	assert response.status_code == 400 or response.status_code == 422

def test_get_items_structure():
	response = client.get("/items")

	assert response.status_code == 200

	for item in response.json():
		assert "title" in item
		assert "price" in item

def test_get_single_item():
	create_payload = {
		"type": "Book",
		"title": "Clean Code",
		"price": 29.99,
		"author": "Robert C. Martin",
		"year": 2008
	}

	create_res = client.post("/items", json=create_payload)
	item_id = create_res.json()["id"]

	response = client.get(f"/items/{item_id}")

	assert response.status_code == 200
	data = response.json()

	assert data["title"] == "Clean Code"

def test_get_single_item_not_found():
	response = client.get("/items/does-not-exist")

	assert response.status_code == 404
	assert "Invalid Item-ID" in response.json()["detail"]

def test_delete_item():
	# create item first
	create = client.post("/items", json={
		"type": "Book",
		"title": "Test",
		"price": 10,
		"author": "X",
		"year": 2020
	})

	item_id = create.json()["id"]

	# delete
	res = client.delete(f"/items/{item_id}")

	assert res.status_code == 204

def test_delete_item_not_found():
	res = client.delete("/items/does-not-exist")

	assert res.status_code == 404

def test_patch_item_success():
	# 1. create item first
	create_payload = {
		"type": "Book",
		"title": "Clean Code",
		"price": 29.99,
		"author": "Robert C. Martin",
		"year": 2008
	}

	create_res = client.post("/items", json=create_payload)
	item_id = create_res.json()["id"]

	# 2. update
	update_payload = {
		"title": "Clean Code (Updated)",
		"price": 39.99
	}

	response = client.put(f"/items/{item_id}", json=update_payload)

	assert response.status_code == 200
	data = response.json()

	assert data["title"] == "Clean Code (Updated)"
	assert data["price"] == 39.99
	print(response.json())

def test_patch_item_empty_update():
	create_res = client.post("/items", json={
		"type": "Book",
		"title": "Clean Code",
		"price": 29.99,
		"author": "Robert C. Martin",
		"year": 2008
	})

	item_id = create_res.json()["id"]

	response = client.put(f"/items/{item_id}", json={})

	assert response.status_code == 400