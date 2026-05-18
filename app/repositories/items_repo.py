import sqlite3

conn = sqlite3.connect("media.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
	id TEXT PRIMARY KEY,
	title TEXT NOT NULL,
	type TEXT NOT NULL,
	price REAL NOT NULL,
	on_loan INTEGER NOT NULL,
	season INTEGER,
	platform TEXT,
	artist TEXT,
	author TEXT,
	year INTEGER
)
""")

def generate_id(prefix):
	cursor.execute(
		"SELECT id FROM inventory WHERE id LIKE ? ORDER BY id DESC LIMIT 1",
		(f"{prefix}%",)
	)

	row = cursor.fetchone()
	if not row:
		return f"{prefix}0001"

	last_id = row[0]
	number = int(last_id[1:]) + 1
	return f"{prefix}{number:04d}"

def load_items():
	cursor.execute("SELECT * FROM inventory")
	return cursor.fetchall()

def load_single_item(item_id: str):
	cursor.execute("""
		SELECT *
		FROM inventory
		WHERE id = ?
	""", (item_id,))
	return cursor.fetchone()

def save_item(item):
	if item.id is None:
		item.id = generate_id(item.prefix)

	cursor.execute("""
		INSERT INTO inventory (
			id, title, type, price, on_loan,
			season, platform, artist, author, year
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	""", (
		item.id,
		item.title,
		type(item).__name__,
		item.price,
		int(item.on_loan),
		getattr(item, "season", None),
		getattr(item, "platform", None),
		getattr(item, "artist", None),
		getattr(item, "author", None),
		getattr(item, "year", None)
	))

	conn.commit()

def delete_item(item_id):
	cursor.execute(
		"DELETE FROM inventory WHERE id = ?",
		(item_id,)
	)
	conn.commit()

	return cursor.rowcount

def update_item(item_id: str, data: dict):
	fields = []
	values = []

	for key, value in data.items():
		if value is not None:
			fields.append(f"{key} = ?")
			values.append(value)

	if not fields:
		return 0

	values.append(item_id)

	query = f"""
		UPDATE inventory
		SET {", ".join(fields)}
		WHERE id = ?
	"""

	cursor.execute(query, values)
	conn.commit()

	return cursor.rowcount

def update_loan_status(item_id: str, status: bool):
	cursor.execute("""
			UPDATE inventory
			SET on_loan = ?
			WHERE id = ?
		""", (int(status), item_id))
	conn.commit()