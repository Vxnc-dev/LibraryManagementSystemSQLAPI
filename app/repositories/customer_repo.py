import sqlite3

conn = sqlite3.connect("media.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
	id TEXT PRIMARY KEY,
	name TEXT NOT NULL,
	borrowed INTEGER NOT NULL,
	returned INTEGER NOT NULL
)
""")

def generate_customer_id():
	cursor.execute("""
		SELECT id
		FROM customers
		ORDER BY id DESC
		LIMIT 1
	""")

	row = cursor.fetchone()

	if not row:
		return "C0001"

	last_id = row[0]
	number = int(last_id[1:]) + 1

	return f"C{number:04d}"

def load_customer_by_id(customer_id: str):
	cursor.execute(
		"SELECT * FROM customers WHERE id = ?",
		(customer_id,)
	)
	return cursor.fetchone()

def save_customer(customer):
	if customer.id is None:
		customer.id = generate_customer_id()

	cursor.execute("""
		INSERT INTO customers (
			id,
			name,
			borrowed,
			returned
		)
		VALUES (?, ?, ?, ?)
	""", (
		customer.id,
		customer.name,
		customer.borrowed,
		customer.returned
	))

	conn.commit()

def del_customer(customer_id: str):
	cursor.execute("""
		DELETE FROM customers
		WHERE id = ?
	""", (customer_id,))
	conn.commit()

def load_customers():
	cursor.execute("""
		SELECT *
		FROM customers
	""")
	return cursor.fetchall()

def load_customer(customer_id: str):
	cursor.execute("""
		SELECT *
		FROM customers
		WHERE id = ?
	""", (customer_id,))
	return cursor.fetchone()

def update_borrowed_count(customer_id: str, borrowed: int):
	cursor.execute("""
		UPDATE customers
		SET borrowed = ?
		WHERE id = ?
	""", (borrowed, customer_id))
	conn.commit()

def update_returned_count(customer_id: str, returned: int):
	cursor.execute("""
		UPDATE customers
		SET returned = ?
		WHERE id = ?
	""", (returned, customer_id))
	conn.commit()
