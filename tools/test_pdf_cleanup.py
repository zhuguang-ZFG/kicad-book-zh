#!/usr/bin/env python3
"""Regression coverage for PDF browser cleanup."""
import importlib
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "yuyu-book"))

pdf = importlib.import_module("yuyu_book.pdf")


def test_browser_closes_when_print_fails() -> None:
    closed: list[bool] = []

    class FakePage:
        def goto(self, *_args, **_kwargs) -> None:
            pass

        def evaluate(self, *_args, **_kwargs) -> bool:
            return True

        def emulate_media(self, *_args, **_kwargs) -> None:
            pass

        def pdf(self, *_args, **_kwargs) -> None:
            raise RuntimeError("print failed")

    class FakeBrowser:
        def new_page(self, **_kwargs) -> FakePage:
            return FakePage()

        def close(self) -> None:
            closed.append(True)

    class FakePlaywright:
        chromium = object()

    class FakeSyncPlaywright:
        def __enter__(self) -> FakePlaywright:
            return FakePlaywright()

        def __exit__(self, *_args) -> bool:
            return False

    with patch("playwright.sync_api.sync_playwright", lambda: FakeSyncPlaywright()), \
            patch.object(pdf, "_launch", lambda _p, _browser: FakeBrowser()):
        try:
            pdf._print_pdf(Path("book.html"), Path("book.pdf"), None)
        except RuntimeError:
            pass
        else:
            raise AssertionError("print failure must propagate")

    assert closed == [True]


if __name__ == "__main__":
    test_browser_closes_when_print_fails()
    print("PDF cleanup regression: OK")
