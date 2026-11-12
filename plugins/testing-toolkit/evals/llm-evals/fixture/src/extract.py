"""Send one invoice to the model and parse the reply."""

import json
import pathlib

import anthropic

PROMPT = pathlib.Path(__file__).parent.parent / "prompts" / "extract.txt"
MODEL = "claude-haiku-5-5"


def extract(invoice_text: str) -> dict:
    """Return the fields of one invoice."""
    prompt = PROMPT.read_text().replace("{{invoice}}", invoice_text)
    reply = anthropic.Anthropic().messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(reply.content[0].text)
