from pydantic import BaseModel
from typing import Optional, Literal, Union

class ItemCreate(BaseModel):
	type: str
	title: str
	price: float

class ItemUpdate(BaseModel):
	title: Optional[str] = None
	price: Optional[float] = None
	on_loan: Optional[bool] = None
	author: Optional[str] = None
	year: Optional[int] = None
	season: Optional[int] = None
	platform: Optional[str] = None
	artist: Optional[str] = None

class BookCreate(ItemCreate):
	type: Literal["Book"]
	author: str
	year: int

class ComicCreate(ItemCreate):
	type: Literal["Comic"]
	author: str
	year: int

class FilmCreate(ItemCreate):
	type: Literal["Film"]
	year: int

class SeriesCreate(ItemCreate):
	type: Literal["Series"]
	season: int

class MusicCreate(ItemCreate):
	type: Literal["Music"]
	artist: str

class GameCreate(ItemCreate):
	type: Literal["Game"]
	platform: str

ItemCreateUnion = Union[
	BookCreate,
	ComicCreate,
	FilmCreate,
	SeriesCreate,
	MusicCreate,
	GameCreate
]