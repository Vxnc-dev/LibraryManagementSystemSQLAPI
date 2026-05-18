import sqlite3

conn = sqlite3.connect("media.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
	item_id TEXT NOT NULL,
	customer_id TEXT NOT NULL
)
""")

def save_loan_pair(item_id: str, customer_id: str):
	cursor.execute("""
		INSERT INTO loans (
			item_id,
			customer_id
		)
		VALUES (?, ?)
	""", (item_id, customer_id))
	conn.commit()

def get_loan_pair(customer_id: str, item_id: str):
		cursor.execute("""
			SELECT *
			FROM loans
			WHERE item_id = ? AND customer_id = ?
		""", (customer_id, item_id))
		return cursor.fetchone()

def load_loan_pairs():
	cursor.execute("""
		SELECT *
		FROM loans
	""")
	return cursor.fetchall()

def delete_loan_pair(item_id: str, customer_id: str):
	cursor.execute("""
		DELETE FROM loans
		WHERE item_id = ? AND customer_id = ?
	""", (item_id, customer_id))
	conn.commit()