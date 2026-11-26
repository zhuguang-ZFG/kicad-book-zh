#!/usr/bin/env python3
"""Regression coverage for product metadata in the generated HTML shell."""
import importlib
import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "yuyu-book"))
sys.path.insert(0, str(ROOT / "tools"))

app = importlib.import_module("yuyu_book.app")
check_book = importlib.import_module("check_book")
source_registry = importlib.import_module("yuyu_book.backmatter").source_registry
photo_figures = importlib.import_module("yuyu_book.render").photo_figures
renumber_figures = importlib.import_module("yuyu_book.render").renumber_figures
page = importlib.import_module("yuyu_book.style").page


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


def test_photos_share_document_order_figure_numbers() -> None:
    doc = (
        '<figure class="diagram"><figcaption>'
        '<span class="fig-no">图 2-9</span><span class="fig-cap">先</span>'
        '</figcaption></figure>'
        '<p><img alt="图2-1 实物" src="illustrations/example.jpg"></p>'
        '<p><em>图 2-1：中间</em></p>'
        '<figure class="illu illu-line"><figcaption>'
        '<span class="fig-no">图 2-1</span><span class="fig-cap">后</span>'
        '</figcaption></figure>'
    )
    doc = photo_figures(doc)
    doc, count = renumber_figures(doc, prefix="2", lang="zh")
    assert count == 3
    numbers = re.findall(r'<span class="fig-no">([^<]+)</span>', doc)
    assert numbers == ["图 2-1", "图 2-2", "图 2-3"]
    # the hand-written caption number ("图 2-1：中间") must be stripped from
    # the printed caption, or the page shows the same figure number twice
    assert "图 2-1：中间" not in doc
    assert '<span class="fig-cap">中间</span>' in doc


def test_source_registry_separates_books_and_deep_links() -> None:
    sources = json.loads((ROOT / "yuyu-book/sources.json").read_text(encoding="utf-8"))
    sources.pop("schema_version", None)
    for key in ("elektor-kicad-like-a-pro-preview", "bogatin-spi-3e", "johnson-hsdd"):
        assert sources[key]["kind"] == "book"
        assert sources[key]["normative"] is False
    assert sources["kicad-source"]["kind"] == "github"
    assert len(sources["kicad-source"]["pinned"]["commit"]) == 40
    for key in ("kicad-docs-eeschema", "kicad-docs-pcbnew", "kicad-docs-cli"):
        assert sources[key]["kind"] == "docs"
        assert sources[key]["url"].startswith("https://docs.kicad.org/10.0/en/")
    html = source_registry(sources, "zh")
    assert "技术书籍（非规范）" in html
    assert "官方库与指南" in html


def test_source_figure_captions_are_sequential() -> None:
    # Source captions must be 1..N per chapter even though the renderer
    # renumbers figures; duplicates hide a future renderer regression.
    assert check_book.source_figure_number_problems() == []


def test_structure_html_limit_covers_readme_claim() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    structure = (ROOT / "STRUCTURE.md").read_text(encoding="utf-8")
    claim = re.search(r"HTML：.*?约\s*([0-9.]+)\s*MB", readme)
    limit = re.search(r"HTML 构建大小 <\s*([0-9.]+)\s*MB", structure)
    assert claim and limit, "README/STRUCTURE must state the HTML size and limit"
    assert float(claim.group(1)) < float(limit.group(1))


def test_html_claim_requires_structure_limit() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text("HTML：约 5.6MB\n", encoding="utf-8")
        with patch.object(check_book, "ROOT", root), patch.object(check_book, "errors", []):
            check_book.check_artifact_claims()
            errors = list(check_book.errors)
        assert any("no build-size limit" in error for error in errors), errors


def test_html_claim_requires_html_artifact() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text("HTML：约 5.6MB\n", encoding="utf-8")
        (root / "STRUCTURE.md").write_text("HTML 构建大小 < 8MB\n", encoding="utf-8")
        book = root / "book"
        (book / "dist").mkdir(parents=True)
        with patch.object(check_book, "ROOT", root), patch.object(check_book, "BOOK", book), patch.object(check_book, "errors", []):
            check_book.check_artifact_claims()
            errors = list(check_book.errors)
        assert any("no HTML artifact" in error for error in errors), errors


if __name__ == "__main__":
    test_page_shell_does_not_embed_foreign_product_metadata()
    test_page_shell_uses_and_escapes_product_metadata()
    test_build_edition_passes_manifest_metadata_to_page_shell()
    test_photos_share_document_order_figure_numbers()
    test_source_figure_captions_are_sequential()
    test_structure_html_limit_covers_readme_claim()
    test_html_claim_requires_structure_limit()
    test_html_claim_requires_html_artifact()
    test_source_registry_separates_books_and_deep_links()
    print("book metadata regression: OK")
