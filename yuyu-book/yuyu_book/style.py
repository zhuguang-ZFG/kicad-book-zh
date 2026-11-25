"""Single-file page shell; ornaments and CSS live in deco/style_css."""
from __future__ import annotations

from html import escape

from .deco import (INK_MARKS, WHEEL_SVG, ink_mark, itinerary, key_mark, knot,
                   route_map, rut, trace, wheel)
from .style_css import CSS

__all__ = ["CSS", "INK_MARKS", "WHEEL_SVG", "ink_mark", "itinerary", "key_mark",
           "knot", "route_map", "rut", "trace", "wheel", "page"]


def page(lang: str, title: str, css: str, body_class: str, content: str,
         rail: str, colophon: str, *, author: str = "",
         description: str = "") -> str:
    fav = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='
           "'http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle "
           "cx='16' cy='16' r='12' fill='none' stroke='%23B4472F' "
           "stroke-width='3'/%3E%3Ccircle cx='16' cy='16' r='4' "
           "fill='%23B4472F'/%3E%3C/svg%3E\">")
    safe_title = escape(title, quote=True)
    safe_author = escape(author, quote=True)
    safe_description = escape(description, quote=True)
    og = (
        f'<meta property="og:title" content="{safe_title}">'
        f'<meta property="og:description" content="{safe_description}">'
        '<meta property="og:type" content="book">'
    )
    return f"""<!doctype html>
<html lang="{'zh-CN' if lang == 'zh' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="author" content="{safe_author}">
<meta name="generator" content="yuyu-book">
{fav}
{og}
<title>{safe_title}</title>
<style>{css}</style>
</head>
<body class="{body_class}">
{rail}
<main class="sheet">
{content}
{colophon}
</main>
</body>
</html>"""
