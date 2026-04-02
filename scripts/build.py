from datetime import date
from pathlib import Path
from shutil import copy

import nbformat
from jinja2 import Environment, FileSystemLoader
from nbconvert import HTMLExporter
from traitlets.config import Config

from .og_image import generate_og_image
from .schemas import (
    Author,
    RegistryEntry,
    load_authors,
    load_registry,
)

ROOT = Path(__file__).parent.parent
BUILD_DIR = ROOT / "build"
TEMPLATE = "template"
SITE_URL = "https://cookbook.columnar.tech"


def copy_static_files() -> None:
    files: list[str] = ["style.css", "favicon.svg", "og.png"]
    for file in files:
        source = ROOT / TEMPLATE / "static" / file
        destination = BUILD_DIR / file
        copy(source, destination)
        print(f"Copied: {source} -> {destination}")


def load_exporter() -> HTMLExporter:
    c = Config()
    c.HTMLExporter.extra_template_basedirs = [str(ROOT)]
    c.HTMLExporter.template_name = TEMPLATE
    return HTMLExporter(config=c)


def format_date(d: date) -> str:
    return d.strftime("%b %-d, %Y")


def build_notebooks(registry: list[RegistryEntry], authors: dict[str, Author]) -> None:
    html_exporter = load_exporter()

    for entry in registry:
        notebook_path = ROOT / entry.path
        notebook_slug = notebook_path.stem
        notebook = nbformat.reads(notebook_path.read_text(encoding="utf-8"), as_version=4)
        notebook.metadata["title"] = entry.title

        og_image_filename = "og.png"
        og_image_path = BUILD_DIR / notebook_slug / og_image_filename
        generate_og_image(
            title=entry.title,
            description=entry.description,
            output_path=og_image_path,
        )
        print(f"Generated: {og_image_path}")

        notebook_meta = {
            "title": entry.title,
            "date": format_date(entry.date),
            "authors": [authors[a] for a in entry.authors],
            "github_url": f"https://github.com/columnar-tech/columnar-cookbook/blob/main/{entry.path}",
            "description": entry.description,
            "og_image_url": f"{SITE_URL}/{notebook_slug}/{og_image_filename}",
            "page_url": f"{SITE_URL}/{notebook_slug}",
        }
        resources = {"notebook_meta": notebook_meta}
        (body, _) = html_exporter.from_notebook_node(notebook, resources=resources)

        build_path = BUILD_DIR / notebook_slug / "index.html"
        build_path.parent.mkdir(exist_ok=True)
        build_path.write_text(body, encoding="utf-8")

        print(f"Converted: {notebook_path} -> {build_path}")


def jinja_environment() -> Environment:
    loader = FileSystemLoader(ROOT / TEMPLATE)
    environment = Environment(loader=loader)
    environment.filters["format_date"] = format_date
    return environment


def build_home_page(registry: list[RegistryEntry], authors: dict[str, Author]) -> None:
    env = jinja_environment()
    template = env.get_template("home.html.j2")
    html = template.render(registry=registry, authors=authors)

    build_path = BUILD_DIR / "index.html"
    build_path.write_text(html, encoding="utf-8")
    print(f"Rendered: {ROOT / TEMPLATE / 'home.html.j2'} -> {build_path}")


if __name__ == "__main__":
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    registry = load_registry()
    authors = load_authors()
    build_notebooks(registry, authors)
    build_home_page(registry, authors)
    copy_static_files()
