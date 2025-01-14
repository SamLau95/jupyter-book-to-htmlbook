import logging
from bs4 import BeautifulSoup  # type: ignore

from jupyter_book_to_htmlbook.footnote_processing import process_footnotes


def test_process_footnotes_happy_path():
    """
    Happy path test for footnote conversions

    Footnote references should be pulled into a span with the
    data-type="footnote" attribute, and the references section
    should be destroyed
    """
    chapter_text = """<div>
<p>For example, Twitter lets people quickly download millions of data
points.<a class="footnote-reference brackets" href="#twitter" id="id1">1</a>
</p>
<hr class="footnotes docutils" />
<dl class="footnote brackets">
<dt class="label" id="twitter">
<span class="brackets"><a class="fn-backref" href="#id1">1</a></span></dt>
<dd><p>Isn't the internet amazing?</p>
</dd></dl></div>"""
    chapter = BeautifulSoup(chapter_text, 'html.parser')
    result = process_footnotes(chapter)
    assert str(result) == """<div>
<p>For example, Twitter lets people quickly download millions of data
points.<span data-type="footnote">Isn't the internet amazing?</span>
</p>

</div>"""


def test_prcoess_footnotes_no_href(caplog):
    """
    Probably would never happen, but in case (for example) the href attr
    was missing on the reference, throw an error showing the footnote ref
    """
    chapter = BeautifulSoup("""<div>Hello, world!</div><hr />
    <a id='test' class='footnote-reference'>something</a>""", 'html.parser')
    result = process_footnotes(chapter)
    assert result == chapter
    caplog.set_level(logging.DEBUG)
    expected_issue = '"<a class="footnote-reference" id="test">something</a>".'
    assert expected_issue in caplog.text


def test_prcoess_footnotes_poorly_formed(caplog):
    """
    Probably might happen; there is some value error going on somewhere, e.g.,
    a bad ref location, so throw an error noting the footnote ref in question
    """
    chapter = BeautifulSoup("""<div>Hello, world!</div><hr />
    <a id="id1" href="na" class='footnote-reference'/>""",
                            'html.parser')
    result = process_footnotes(chapter)
    assert result == chapter
    caplog.set_level(logging.DEBUG)
    expected_issue = '"<a class="footnote-reference" href="na" id="id1"></a>".'
    assert expected_issue in caplog.text
