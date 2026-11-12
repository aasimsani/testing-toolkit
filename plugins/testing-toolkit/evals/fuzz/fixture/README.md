# tinycfg

`tinycfg/parser.py` reads the config files that customers upload. The bytes are untrusted.

## Contract

1. `parse_config(data: bytes)` returns a dict of sections, and each section is a dict of string keys and string values.
2. For any input it can't parse, it raises `ConfigError`. It raises nothing else, and it always returns.
3. `dump_config(config)` writes a config back out as bytes. `parse_config(dump_config(c)) == c` for every `c` that `parse_config` returned.

`samples/` holds three real config files.

Last month a customer upload crashed the import worker, so this parser now needs a fuzz harness. CI will run it with Atheris.
