---
type: llm
weight: 2
focus: {source: file, path: tests/test_rle_properties.py}
---

Pass if the file has a property about the encoded output itself, beyond the round trip. Examples: neighbouring runs never share a letter, the run lengths add up to the length of the input, or the output matches the run format.

Fail if the round trip is the only property over valid input.
