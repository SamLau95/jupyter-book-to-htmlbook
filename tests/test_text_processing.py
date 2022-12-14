from bs4 import BeautifulSoup  # type: ignore
from jupyter_book_to_htmlbook.text_processing import (
    clean_chapter,
    move_span_ids_to_sections,
    process_sidebars
    )


def test_chapter_cleans():
    """ test that we're ripping out the things we want to """
    chapter_text = r"""<style>body: 13px</style>
<script src="js/js.js" />
<table border="7">
<tr><td>Hello</td><td>World</td></tr>
</table>
<p style="text-decoration: underline">Lorem ipsum</p>
<h2><span class="section-number">19.1.1.
</span>Issues with Linear Regression<a class="headerlink"
href="#issues-with-linear-regression" title="Permalink to this headline">¶</a>
/h2>
<div class="cell tag_hide-input docutils container">
div class="cell_input docutils container">
<pre> some thing </pre>
</div>
</div>"""
    chapter = BeautifulSoup(chapter_text, 'html.parser')
    result = clean_chapter(chapter)
    assert str(result) == """

<table>
<tr><td>Hello</td><td>World</td></tr>
</table>
<p>Lorem ipsum</p>
<h2>Issues with Linear Regression
/h2&gt;
<div class="cell tag_hide-input docutils container">
div class="cell_input docutils container"&gt;
<pre> some thing </pre>
</div>
</h2>"""


def test_move_span_ids_to_sections():
    """
    Atlas requires that cross reference targets sections so that
    the text will appear as expected. This test is to confirm that
    the ids we added ("sec-") to the invisible spans earlier for cross
    referencing are then applied to the parent section.
    """
    chapter_text = """
<section class="section" data-type="sect2" id="types-of-bias">
<span id="sec-biastypes"></span><h2>Types of Bias</h2>
<p>Bias comes in many forms!</p>"""
    chapter = BeautifulSoup(chapter_text, 'html.parser')
    result = move_span_ids_to_sections(chapter)
    assert str(result) == """
<section class="section" data-type="sect2" id="sec-biastypes">
<h2>Types of Bias</h2>
<p>Bias comes in many forms!</p></section>"""


def test_sidebar_processing():
    """
    Sidebars from jupyter book (from the ```{sidebar} syntax) are
    formatted as <aside>s with a "sidebar" class. For HTMLBook, these
    need to have sidebar data-types, and the paragraph with the
    "sidebar-title" class should be an <h5> element.
    """
    chapter_text = BeautifulSoup("""<aside class="sidebar">
<p class="sidebar-title">Here Is a Sidebar Title</p>
<p>And this is some sidebar content!</p>
</div>
</aside>""", "html.parser")
    process_sidebars(chapter_text)
    assert chapter_text.find("aside")["data-type"] == "sidebar"
    assert chapter_text.find("h5").string == "Here Is a Sidebar Title"
