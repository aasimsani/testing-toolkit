"""A small INI-like config parser for customer uploads."""


class ConfigError(Exception):
    """The input is not a valid config file."""


def parse_config(data: bytes) -> dict[str, dict[str, str]]:
    """Parse ``data`` into sections of key/value pairs."""
    text = data.decode("utf-8")
    config: dict[str, dict[str, str]] = {}
    section = None
    for number, raw in enumerate(text.split("\n"), start=1):
        line = raw.strip()
        if not line or line[0] == "#":
            continue
        if line[0] == "[":
            if line[-1] != "]" or len(line) < 3:
                raise ConfigError(f"line {number}: bad section header")
            section = line[1:-1].strip()
            if section in config:
                raise ConfigError(f"line {number}: duplicate section {section!r}")
            config[section] = {}
            continue
        if section is None:
            raise ConfigError(f"line {number}: key outside a section")
        key, sep, value = line.partition("=")
        if not sep:
            raise ConfigError(f"line {number}: missing '='")
        key = key.strip()
        if key[0].isdigit():
            raise ConfigError(f"line {number}: key starts with a digit")
        config[section][key] = value.strip()
    return config


def dump_config(config: dict[str, dict[str, str]]) -> bytes:
    """Write ``config`` in the format that ``parse_config`` reads."""
    lines = []
    for section, pairs in config.items():
        lines.append(f"[{section}]")
        for key, value in pairs.items():
            lines.append(f"{key} = {value}")
        lines.append("")
    return "\n".join(lines).encode("utf-8")
