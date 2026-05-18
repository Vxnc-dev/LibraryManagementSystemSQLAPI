from app.schemas.item_schemas import BookCreate, FilmCreate, SeriesCreate, ComicCreate, GameCreate, MusicCreate
from app.models.item import Book, Film, Series, Music, Game, Comic

def build_item_from_schema(data):
	if isinstance(data, BookCreate):
		return Book(
			title=data.title,
			author=data.author,
			year=data.year,
			price=data.price
		)

	elif isinstance(data, FilmCreate):
		return Film(
			title=data.title,
			year=data.year,
			price=data.price
		)

	elif isinstance(data, SeriesCreate):
		return Series(
			title=data.title,
			season=data.season,
			price=data.price
		)

	elif isinstance(data, ComicCreate):
		return Comic(
			title=data.title,
			author=data.author,
			year=data.year,
			price=data.price
		)

	elif isinstance(data, MusicCreate):
		return Music(
			title=data.title,
			artist=data.artist,
			price=data.price
		)

	elif isinstance(data, GameCreate):
		return Game(
			title=data.title,
			platform=data.platform,
			price=data.price
		)

	raise ValueError("Unknown item type")