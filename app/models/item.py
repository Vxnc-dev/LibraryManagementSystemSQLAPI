from typing import Any

class Media:
	def __init__(self, title: str, price: float):
		self.id = None
		self.title = title
		self.price = price
		self.on_loan = False

	def identity_key(self) -> tuple[Any, ...]:
		return self.__class__.__name__, self.title

	def same_identity(self, other):
		return (
			isinstance(other, self.__class__)
			and self.identity_key() == other.identity_key()
		)

	def __eq__(self, other):
		return (
				type(self) is type(other)
				and self.__dict__ == other.__dict__
		)


class Book(Media):
	prefix = "B"

	def __init__(self, title: str, author: str, year: int, price: float):
		super().__init__(title, price)
		self.author = author
		self.year = year

	def identity_key(self) -> tuple[Any, ...]:
		return super().identity_key() + (self.author, self.year)


class Comic(Media):
	prefix = "C"

	def __init__(self, title: str, author: str, year: int, price: float):
		super().__init__(title, price)
		self.author = author
		self.year = year

	def identity_key(self):
		return super().identity_key() + (self.author, self.year)


class Film(Media):
	prefix = "F"

	def __init__(self, title: str, year: int, price: float):
		super().__init__(title, price)
		self.year = year

	def identity_key(self):
		return super().identity_key() + (self.year,)


class Series(Media):
	prefix = "S"

	def __init__(self, title: str, season: int, price: float):
		super().__init__(title, price)
		self.season = season

	def identity_key(self):
		return super().identity_key() + (self.season,)


class Music(Media):
	prefix = "M"

	def __init__(self, title: str, artist: str, price: float):
		super().__init__(title, price)
		self.artist = artist

	def identity_key(self):
		return super().identity_key() + (self.artist,)


class Game(Media):
	prefix = "G"

	def __init__(self, title: str, platform: str, price: float):
		super().__init__(title, price)
		self.platform = platform

	def identity_key(self):
		return super().identity_key() + (self.platform,)