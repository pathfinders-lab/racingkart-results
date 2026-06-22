from template import page


def test_page_wraps_body_with_doctype_and_title():
    html = page("My Title", "<p>hi</p>")
    assert html.startswith("<!DOCTYPE html>")
    assert "My Title" in html
    assert "<p>hi</p>" in html
