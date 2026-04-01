from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = Path(__file__).parent.parent / "template" / "fonts"


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    font_file = FONTS_DIR / ("Inter-Bold.ttf" if bold else "Inter-Regular.ttf")
    return ImageFont.truetype(str(font_file), size)


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current: list[str] = []

    for word in text.split():
        test_line = " ".join([*current, word])
        if font.getbbox(test_line)[2] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]

    if current:
        lines.append(" ".join(current))
    return lines


def draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    x: int,
    y: int,
    max_width: int,
    max_lines: int,
    fill: str,
) -> int:
    lines = wrap_text(text, font, max_width)[:max_lines]
    ascent, descent = font.getmetrics()
    line_height = ascent + descent + 8
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_height), line, fill=fill, font=font)
    return len(lines) * line_height


def generate_og_image(title: str, description: str, output_path: str | Path) -> None:
    width, height = 1200, 630
    padding = 80
    max_text_width = width - padding * 2

    img = Image.new("RGB", (width, height), "#434343")
    draw = ImageDraw.Draw(img)

    title_height = draw_wrapped_text(
        draw=draw,
        text=title,
        font=get_font(64, bold=True),
        x=padding,
        y=padding,
        max_width=max_text_width,
        max_lines=3,
        fill="white",
    )

    draw_wrapped_text(
        draw=draw,
        text=description,
        font=get_font(38),
        x=padding,
        y=padding + title_height + 40,
        max_width=max_text_width,
        max_lines=4,
        fill="#999999",
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
