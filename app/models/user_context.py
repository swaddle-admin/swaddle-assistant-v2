from pydantic import BaseModel
from typing import Any


class Location(BaseModel):
    address: str | None = None
    city: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class User(BaseModel):
    id: int
    name: str | None = None
    email: str | None = None
    caretaker_role: str | None = None
    number_of_children: int | None = None
    location: Location | None = None


class Favorites(BaseModel):
    children_likes: Any | None = None
    parent_likes: Any | None = None
    parks: Any | None = None
    restaurants: Any | None = None


class Child(BaseModel):
    id: int
    name: str | None = None
    birthday: str | None = None
    gender: str | None = None
    interests: Any | None = None


class UserContext(BaseModel):
    user: User | None = None
    favorites: Favorites | None = None
    children: list[Child] = []