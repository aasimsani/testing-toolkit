"""Run-length codec for strings of the letters a to z."""

import re

_RUN = re.compile(r"([1-9][0-9]*)([a-z])")


def encode(text: str) -> str:
    """Return the run-length encoding of ``text``."""
    out = []
    i = 0
    while i < len(text):
        letter = text[i]
        if not "a" <= letter <= "z":
            raise ValueError(f"not a lowercase letter: {letter!r}")
        j = i
        while j < len(text) and text[j] == letter:
            j += 1
        out.append(f"{j - i}{letter}")
        i = j
    return "".join(out)


def decode(encoded: str) -> str:
    """Return the text that ``encode`` turned into ``encoded``."""
    out = []
    pos = 0
    previous = None
    while pos < len(encoded):
        match = _RUN.match(encoded, pos)
        if match is None:
            raise ValueError(f"malformed run at offset {pos}")
        count, letter = int(match.group(1)), match.group(2)
        if letter == previous:
            raise ValueError(f"two neighbouring runs of {letter!r}")
        out.append(letter * count)
        previous = letter
        pos = match.end()
    return "".join(out)
