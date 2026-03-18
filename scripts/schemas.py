from datetime import date
from pathlib import Path

from pydantic import BaseModel, HttpUrl, TypeAdapter

_ROOT = Path(__file__).parent.parent


class RegistryEntry(BaseModel):
    title: str
    path: str
    date: date
    authors: list[str]
    description: str


class Author(BaseModel):
    name: str
    avatar: HttpUrl


def load_registry() -> list[RegistryEntry]:
    return TypeAdapter(list[RegistryEntry]).validate_json((_ROOT / "registry.json").read_bytes())


def load_authors() -> dict[str, Author]:
    return TypeAdapter(dict[str, Author]).validate_json((_ROOT / "authors.json").read_bytes())
