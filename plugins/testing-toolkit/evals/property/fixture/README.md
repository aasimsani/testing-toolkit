# textcodec

`textcodec/rle.py` is a run-length codec for strings of lowercase letters.

## Rules

1. `encode(text)` turns each run of one letter into its length followed by the letter: `encode("aaab") == "3a1b"`. The empty string encodes to the empty string.
2. `decode(encoded)` reverses `encode`. For every string `text` of the letters a to z, `decode(encode(text)) == text`.
3. In the output of `encode`, two neighbouring runs never have the same letter.
4. `encode` accepts only the letters a to z. Any other character raises `ValueError`.
5. `decode` raises `ValueError` for input that `encode` could not have produced, such as `"a3"`, `"0a"` or `"2a3a"`.

## Running tests

```bash
.venv/bin/python -m pytest -q
```
