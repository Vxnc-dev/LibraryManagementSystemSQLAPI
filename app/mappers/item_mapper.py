from app.models.item import Book, Film, Comic, Music, Series, Game


def _row_to_item(row):
	(
		item_id, title, media_type, price,
		on_loan, season, platform, artist, author, year
	) = row

	if media_type == "Book":
		item = Book(title, author, year, price)

	elif media_type == "Film":
		item = Film(title, year, price)

	elif media_type == "Comic":
		item = Comic(title, author, year, price)

	elif media_type == "Series":
		item = Series(title, season, price)

	elif media_type == "Music":
		item = Music(title, artist, price)

	elif media_type == "Game":
		item = Game(title, platform, price)

	else:
		return None

	item.id = item_id
	item.on_loan = bool(on_loan)

	return item