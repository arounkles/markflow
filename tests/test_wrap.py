import textwrap

from markflow.formatters.textwrap import (
    code_split,
    link_split,
    newline_split,
    space_split,
    wrap,
)


class TestWrap:
    def test_all_splits(self) -> None:
        input_ = (
            "abc abc abc abc abc abc abc abc abc ``abc ``` abc[0][0] ``abc abc abc abc "
            "<br /><br /> abc abc [url](http://example.com) "
            "abc[url][http://example.com]abc[url][URL][url][URL]  <br/>abc<br/>"
        )
        expected = textwrap.dedent(
            """\
            abc abc abc abc abc abc abc abc abc
            ``abc ``` abc[0][0] ``abc abc abc abc <br />
            <br />
            abc abc [url](http://example.com) abc[url][
            http://example.com]abc[url][URL][url][URL] <br/>
            abc<br/>"""
        )
        assert wrap(input_, 50) == expected

    def test_code_split(self) -> None:
        input_ = "a` a `` b` a `b`c"
        expected_split_text = ["a", "` a `` b`", "a", "`b`", "c"]
        expected_leading_spaces = [False, False, True, True, False]
        expected_evaluates = [True, False, True, False, True]
        split_text, leading_spaces, evaluates = code_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_code_split_begin_and_end(self) -> None:
        input_ = "` a `` b` a `b`"
        expected_split_text = ["` a `` b`", "a", "`b`"]
        expected_leading_spaces = [False, True, True]
        expected_evaluates = [False, True, False]
        split_text, leading_spaces, evaluates = code_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_code_split_sentence(self) -> None:
        input_ = "a` a `` b`. a `b`.c"
        expected_split_text = ["a", "` a `` b`.", "a", "`b`.", "c"]
        expected_leading_spaces = [False, False, True, True, False]
        expected_evaluates = [True, False, True, False, True]
        split_text, leading_spaces, evaluates = code_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_code_split_solo_tilda(self) -> None:
        input_ = "` a `` b` a `b` `a"
        expected_split_text = ["` a `` b`", "a", "`b`", "`a"]
        expected_leading_spaces = [False, True, True, True]
        expected_evaluates = [False, True, False, True]
        split_text, leading_spaces, evaluates = code_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_link_split(self) -> None:
        input_ = "a[URL][url] b [URL](http://example.com)c"
        expected_split_text = [
            "a",
            "[URL][",
            "url]",
            "b",
            "[URL](",
            "http://example.com)",
            "c",
        ]
        expected_leading_spaces = [False, False, False, True, True, False, False]
        expected_evaluates = [True, True, False, True, True, False, True]
        split_text, leading_spaces, evaluates = link_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_link_split_sentence(self) -> None:
        input_ = "a[URL][url]. b [URL](http://example.com).c"
        expected_split_text = [
            "a",
            "[URL][",
            "url].",
            "b",
            "[URL](",
            "http://example.com).",
            "c",
        ]
        expected_leading_spaces = [False, False, False, True, True, False, False]
        expected_evaluates = [True, True, False, True, True, False, True]
        split_text, leading_spaces, evaluates = link_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_newline_split(self) -> None:
        input_ = "a <br /> b <br>c<br/>d"
        expected_split_text = ["a", "<br />", "b", "<br>", "c", "<br/>", "d"]
        expected_leading_spaces = [False, True, True, True, False, False, False]
        expected_evaluates = [True, False, True, False, True, False, True]
        split_text, leading_spaces, evaluates = newline_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_space_split(self) -> None:
        input_ = " ".join(["a"] * 10)
        expected_split_text = ["a"] * 10
        expected_leading_spaces = [False] + [True] * 9
        expected_evaluates = [True] * 10
        split_text, leading_spaces, evaluates = space_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates
