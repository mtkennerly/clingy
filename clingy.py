import argparse
import email
from email.message import Message
from fnmatch import fnmatch
import os
import re


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Save attachments from plain text email files.")

    parser.add_argument(
        "filenames", type=str, nargs="+", help="filenames of emails from which to save attachments"
    )

    parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        help="directory for saving (default is working directory)",
    )

    parser.add_argument(
        "-g",
        "--glob",
        dest="glob",
        metavar="PATTERN",
        help="glob pattern to filter attachments by name",
    )

    parser.add_argument(
        "-r",
        "--regex",
        dest="regex",
        metavar="PATTERN",
        help="regular expression to filter attachments by name",
    )

    return parser.parse_args(argv)


def find(source, glob=None, regex=None):
    """
    Find all attachments in an email.

    :param str source: Filename or plain text of an email
    :param str glob: Glob pattern
    :param str regex: Regular expression
    :return: List of attachments
    :rtype: list[email.message.Message]
    """

    if os.path.isfile(source):
        with open(source) as file:
            source = file.read()

    message = email.message_from_string(source)

    attachments = []
    for payload in message.get_payload():
        filename = payload.get_filename()

        if filename and match(filename, glob, regex):
            attachments.append(payload)

    return attachments


def match(string, glob=None, regex=None):
    """
    Match a string against a glob pattern and/or regular expression.

    :param str string: String to match against patterns
    :param str glob: Glob pattern
    :param str regex: Regular expression
    :return: True if string matches all specified patterns, otherwise False
    :rtype: bool
    """

    matches_glob = fnmatch(string, glob) if glob else True
    matches_regex = re.search(regex, string) is not None if regex else True

    return matches_glob and matches_regex


def save(source, directory=None, glob=None, regex=None):
    """
    Save all attachments from an email.

    :param source: Filename, plain text, or message object of an email.
    :type source: str or email.message.Message
    :param str directory: Directory in which to save attachments.
        Defaults to current working directory.
    :param str glob: Glob pattern
    :param str regex: Regular expression
    :return: None
    """

    if isinstance(source, Message):
        attachments = [source]
    else:
        attachments = find(source)

    for attachment in attachments:
        filename = attachment.get_filename()

        if not match(filename, glob, regex):
            continue

        if directory:
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = os.path.join(directory, filename)

        with open(filename, "wb") as file:
            file.write(attachment.get_payload(decode=True))


def main():
    args = _parse_args()

    for filename in args.filenames:
        if not os.path.exists(filename):
            raise IOError("File not found: {}".format(filename))

    for filename in args.filenames:
        save(filename, args.directory, args.glob, args.regex)


if __name__ == "__main__":
    main()
