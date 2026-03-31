from datetime import date
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, Field, HttpUrl, TypeAdapter

_ROOT = Path(__file__).parent.parent

Category = Literal["Database Connections", "Data Loading", "Data Analysis"]


class RegistryEntry(BaseModel):
    title: str
    path: str
    date: date
    authors: Annotated[list[str], Field(min_length=1)]
    description: str
    categories: Annotated[list[Category], Field(min_length=1)]


class Author(BaseModel):
    name: str
    avatar: HttpUrl


def load_registry() -> list[RegistryEntry]:
    return TypeAdapter(list[RegistryEntry]).validate_json((_ROOT / "registry.json").read_bytes())


def load_authors() -> dict[str, Author]:
    return TypeAdapter(dict[str, Author]).validate_json((_ROOT / "authors.json").read_bytes())
