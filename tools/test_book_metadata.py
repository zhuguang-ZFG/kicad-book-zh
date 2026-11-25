#!/usr/bin/env python3
"""Regression coverage for product metadata in the generated HTML shell."""
import sys
from tempfile import TemporaryDirectory
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "yuyu-book"))

from yuyu_book import app  # noqa: E402
from yuyu_book.style import page  # noqa: E402


def test_page_shell_does_not_embed_foreign_product_metadata() -> None:
    html = page(
        "zh", "KiCad handbook — KKiCad 教学组", "", "lang-zh", "", "", ""
    )
    assert "LinTsinghua" not in html
    assert "Claude Code" not in html
    assert 'property="og:image" content="cover.png"' not in html


def test_page_shell_uses_and_escapes_product_metadata() -> None:
    html = page(
        "zh",
        "KiCad <guide> & docs",
        "",
        "lang-zh",
        "",
        "",
        "",
        author='KKiCad "教学组" & tools',
        description="从原理图到 Gerber <内容> & 细节",
    )
    assert '<meta name="author" content="KKiCad &quot;教学组&quot; &amp; tools">' in html
    assert '<meta property="og:title" content="KiCad &lt;guide&gt; &amp; docs">' in html
    assert '<meta property="og:description" content="从原理图到 Gerber &lt;内容&gt; &amp; 细节">' in html
    assert "<title>KiCad &lt;guide&gt; &amp; docs</title>" in html


def test_build_edition_passes_manifest_metadata_to_page_shell() -> None:
    manifest = {
        "title": {"zh": "KiCad guide"},
        "author": 'KKiCad "teaching" & tools',
        "subtitle": {"zh": "From schematic to Gerber <guide> & details"},
        "parts": [],
        "product": "book",
        "output_prefix": "metadata-regression",
    }
    assembly = SimpleNamespace(
        body=[], rail=[], units=[], payloads=[], expect_svgs=None,
        n_diagrams=0,
    )
    counts = {
        "marks": 0, "lead": 0, "chips": 0,
        "emblems": 0, "heads": 0, "keeper": 0,
    }

    with TemporaryDirectory() as temp_dir:
        with (
            patch.object(app, "assemble_book", return_value=assembly),
            patch.object(app.render, "soften_long_names", side_effect=lambda html: html),
            patch.object(app, "_audit", return_value=counts),
        ):
            output = app.build_edition(
                "zh", manifest, {}, mode="source", browser=None,
                autolink=False, out_dir=Path(temp_dir), do_pdf=False,
                edge=None,
            )

        html = output.read_text(encoding="utf-8")
        assert '<meta name="author" content="KKiCad &quot;teaching&quot; &amp; tools">' in html
        assert (
            '<meta property="og:description" '
            'content="From schematic to Gerber &lt;guide&gt; &amp; details">'
        ) in html
        assert "LinTsinghua" not in html
        assert "Claude Code" not in html
        assert "cover.png" not in html


if __name__ == "__main__":
    test_page_shell_does_not_embed_foreign_product_metadata()
    test_page_shell_uses_and_escapes_product_metadata()
    test_build_edition_passes_manifest_metadata_to_page_shell()
    print("book metadata regression: OK")
