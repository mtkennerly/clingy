from pathlib import Path
from unittest import mock

import pytest

import clingy

REPO = Path(__file__).parent.parent
EMAIL = REPO / "tests" / "email.txt"


def test__parse_args_need_at_least_one_filename():
    with pytest.raises(SystemExit):
        clingy._parse_args([])


def test__parse_args_one_email():
    argv = ["email.txt"]
    args = clingy._parse_args(argv)
    assert args.filenames == argv


def test__parse_args_multiple_emails():
    argv = ["email1.txt", "email2.txt"]
    args = clingy._parse_args(argv)
    assert args.filenames == argv


def test__parse_args_directory_short():
    argv = ["email.txt", "-d", "out"]
    args = clingy._parse_args(argv)
    assert args.filenames == ["email.txt"]
    assert args.directory == "out"


def test__parse_args_directory_long():
    argv = ["email.txt", "--directory", "out"]
    args = clingy._parse_args(argv)
    assert args.filenames == ["email.txt"]
    assert args.directory == "out"


def test__parse_args_glob_short():
    argv = ["email.txt", "-g", "*.txt"]
    args = clingy._parse_args(argv)
    assert args.filenames == ["email.txt"]
    assert args.glob == "*.txt"


def test__parse_args_glob_long():
    argv = ["email.txt", "--glob", "*.txt"]
    args = clingy._parse_args(argv)
    assert args.filenames == ["email.txt"]
    assert args.glob == "*.txt"


def test__parse_args_regex_short():
    argv = ["email.txt", "-r", r"\.txt$"]
    args = clingy._parse_args(argv)
    assert args.filenames == ["email.txt"]
    assert args.regex == r"\.txt$"


def test__parse_args_regex_long():
    argv = ["email.txt", "--regex", r"\.txt$"]
    args = clingy._parse_args(argv)
    assert args.filenames == ["email.txt"]
    assert args.regex == r"\.txt$"


def test_find_with_filename():
    attachments = clingy.find(EMAIL)

    assert len(attachments) == 2
    assert attachments[0].get_filename() == "foo.txt"
    assert attachments[1].get_filename() == "bar.txt"


def test_find_with_glob():
    attachments = clingy.find(EMAIL, glob="foo*")

    assert len(attachments) == 1
    assert attachments[0].get_filename() == "foo.txt"


def test_find_with_regex():
    attachments = clingy.find(EMAIL, regex=r"^foo")

    assert len(attachments) == 1
    assert attachments[0].get_filename() == "foo.txt"


def test_find_with_string():
    email = EMAIL.read_text()
    attachments = clingy.find(email)

    assert len(attachments) == 2
    assert attachments[0].get_filename() == "foo.txt"
    assert attachments[1].get_filename() == "bar.txt"


def test_match_none():
    assert clingy.match("") is True
    assert clingy.match("foo") is True


def test_match_glob():
    assert clingy.match("foo.txt", glob="*.txt") is True
    assert clingy.match("foo.txt", glob="*.pdf") is False


def test_match_regex():
    assert clingy.match("foo.txt", regex=r"^.+\.txt$") is True
    assert clingy.match("foo.txt", regex=r"^.+\.pdf$") is False


def test_match_both():
    assert clingy.match("foo.txt", glob="*.txt", regex=r"\.txt") is True
    assert clingy.match("foo.txt", glob="*.txt", regex=r"\.pdf") is False


def test_save_with_filename():
    email = EMAIL.read_text()

    mo = mock.mock_open(read_data=email)
    with mock.patch("builtins.open", mo):
        clingy.save(email)

    # Output filenames
    assert mock.call("foo.txt", "wb") in mo.mock_calls
    assert mock.call("bar.txt", "wb") in mo.mock_calls

    # Output file content
    handle = mo()
    assert mock.call(b"foo") in handle.write.mock_calls
    assert mock.call(b"bar") in handle.write.mock_calls


def test_save_with_glob():
    email = EMAIL.read_text()

    mo = mock.mock_open()
    with mock.patch("builtins.open", mo):
        clingy.save(email, glob="bar*")

    # Output filenames
    assert mock.call("bar.txt", "wb") in mo.mock_calls

    # Output file content
    handle = mo()
    assert mock.call(b"bar") in handle.write.mock_calls


def test_save_with_message_object():
    attachments = clingy.find(EMAIL)

    mo = mock.mock_open()
    with mock.patch("builtins.open", mo):
        clingy.save(attachments[0])

    # Output filenames
    assert mock.call("foo.txt", "wb") in mo.mock_calls

    # Output file content
    handle = mo()
    assert mock.call(b"foo") in handle.write.mock_calls


def test_save_with_regex():
    email = EMAIL.read_text()

    mo = mock.mock_open()
    with mock.patch("builtins.open", mo):
        clingy.save(email, glob="bar*")

    # Output filenames
    assert mock.call("bar.txt", "wb") in mo.mock_calls

    # Output file content
    handle = mo()
    assert mock.call(b"bar") in handle.write.mock_calls


def test_save_with_string():
    email = EMAIL.read_text()

    mo = mock.mock_open()
    with mock.patch("builtins.open", mo):
        clingy.save(email)

    # Output filenames
    assert mock.call("foo.txt", "wb") in mo.mock_calls
    assert mock.call("bar.txt", "wb") in mo.mock_calls

    # Output file content
    handle = mo()
    assert mock.call(b"foo") in handle.write.mock_calls
    assert mock.call(b"bar") in handle.write.mock_calls
