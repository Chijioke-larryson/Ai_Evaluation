"""Optional OpenAI-compatible provider adapter using the standard library."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class ProviderError(RuntimeError):
    """A user-facing provider configuration or request error."""


def provider_configured() -> bool:
    return bool(os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_MODEL"))


def generate_response(prompt: str, *, timeout: int = 30) -> str:
    """Request a response from an OpenAI-compatible endpoint when configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
    if not api_key or not model:
        raise ProviderError("Optional provider is not configured. Set OPENAI_API_KEY and OPENAI_MODEL.")
    payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    request = urllib.request.Request(endpoint, data=payload, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise ProviderError("Provider authentication failed. Check the configured API key.") from exc
        if exc.code == 429:
            raise ProviderError("Provider rate limit reached. Try again later.") from exc
        raise ProviderError(f"Provider returned HTTP {exc.code}.") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ProviderError("Provider request timed out or could not connect.") from exc
    except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise ProviderError("Provider returned an unexpected response format.") from exc
    try:
        return str(body["choices"][0]["message"]["content"])
    except (KeyError, IndexError, TypeError) as exc:
        raise ProviderError("Provider response did not contain message content.") from exc

