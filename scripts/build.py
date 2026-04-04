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


def get_og_mtime() -> float:
    paths = [ROOT / "registry.json", ROOT / "scripts" / "og_image.py"]
    paths.extend((ROOT / TEMPLATE / "fonts").rglob("*"))
    mtimes = [p.stat().st_mtime for p in paths if p.is_file()]
    return max(mtimes) if mtimes else 0.0

def get_html_mtime() -> float:
    paths = []
    paths.extend((ROOT / TEMPLATE).rglob("*.j2"))
    paths.append(ROOT / "scripts" / "build.py")
    paths.append(ROOT / "registry.json")
    paths.append(ROOT / "authors.json")
    mtimes = [p.stat().st_mtime for p in paths if p.is_file()]
    return max(mtimes) if mtimes else 0.0

def build_notebooks(registry: list[RegistryEntry], authors: dict[str, Author]) -> None:
    html_exporter = load_exporter()
    html_mtime = get_html_mtime()
    og_mtime = get_og_mtime()

    for entry in registry:
        notebook_path = ROOT / entry.path
        notebook_slug = notebook_path.stem
        nb_mtime = notebook_path.stat().st_mtime
        
        build_path = BUILD_DIR / notebook_slug / "index.html"
        og_image_filename = "og.png"
        og_image_path = BUILD_DIR / notebook_slug / og_image_filename
        
        needs_html = True
        if build_path.exists():
            if build_path.stat().st_mtime >= max(nb_mtime, html_mtime):
                needs_html = False

        needs_og = True
        if og_image_path.exists():
            if og_image_path.stat().st_mtime >= max(nb_mtime, og_mtime):
                needs_og = False

        if not needs_html and not needs_og:
            continue

        notebook = nbformat.reads(notebook_path.read_text(encoding="utf-8"), as_version=4)
        notebook.metadata["title"] = entry.title

        if needs_og:
            generate_og_image(
                title=entry.title,
                description=entry.description,
                output_path=og_image_path,
            )
            print(f"Generated: {og_image_path}")

        if needs_html:
            notebook_meta = {
                "title": entry.title,
                "date": format_date(entry.date),
                "authors": [authors[a] for a in entry.authors],
                "github_url": f"https://github.com/columnar-tech/columnar-cookbook/blob/main/{entry.path}",
                "description": entry.description,
                "categories": entry.categories,
                "og_image_url": f"{SITE_URL}/{notebook_slug}/{og_image_filename}",
                "page_url": f"{SITE_URL}/{notebook_slug}",
            }
            resources = {"notebook_meta": notebook_meta}
            (body, _) = html_exporter.from_notebook_node(notebook, resources=resources)

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
