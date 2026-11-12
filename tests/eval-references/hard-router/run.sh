# The outbox tests need Docker, so this runs the two files that need none.
uv run -q --no-project --with pytest --with requests --with responses python -m pytest -q tests/test_quiet_hours.py tests/test_sms_client.py
