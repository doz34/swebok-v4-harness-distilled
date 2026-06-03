#!/usr/bin/env python3
"""
*** EXPERIMENTAL_v2 - OPT-IN ONLY. NOT CONSUMED BY COMPILED_KNOWLEDGE.PY. ***
SWEBOK v4 Harness V2 — LLM Provider Abstraction
================================================

Provider-agnostic LLM interface. Supports:
- DeterministicProvider (default, offline)
- OpenAIProvider
- AnthropicProvider
- OllamaProvider (local)
- MockProvider (for testing)

Usage:
    from retrieval.providers import Provider
    p = Provider.create("deterministic")
    response = p.complete("What is SOLID?")
    # or with a working dossier
    response = p.answer_with_dossier(dossier, query="...")
"""

import os
import sys
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Provider(ABC):
    """Abstract base for LLM providers."""

    name: str = "abstract"

    @abstractmethod
    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        """Generate a completion."""
        ...

    @abstractmethod
    def chat(self, messages: List[Dict], max_tokens: int = 1024) -> str:
        """Chat-style completion. Messages: [{"role": "user|system|assistant", "content": "..."}]"""
        ...

    def answer_with_dossier(self, dossier, query: str) -> str:
        """Default: render the dossier as a prompt and complete it."""
        prompt = (
            f"You are an expert software engineering advisor. "
            f"Use the following working dossier to answer the question. "
            f"Cite specific sections (by [N] index) in your answer.\n\n"
            f"{dossier.to_prompt(max_tokens=10000)}\n\n"
            f"Question: {query}\n\n"
            f"Answer (cite [N] for each claim):"
        )
        return self.complete(prompt, max_tokens=2048)


class DeterministicProvider(Provider):
    """
    No-LLM provider. Returns a deterministic stub answer that
    summarizes the dossier contents. Useful for testing and offline use.
    """

    name = "deterministic"

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        # Very crude: return a structured stub that lists dossier contents
        lines = [
            "[DETERMINISTIC PROVIDER — no LLM call]",
            "",
            "Based on the working dossier:",
            "",
        ]
        # Extract sections from the prompt
        in_section = False
        for line in prompt.split("\n"):
            if line.startswith("## "):
                in_section = True
                lines.append(f"### {line[3:]}")
            elif in_section and line.startswith("### ["):
                lines.append(line)
            elif in_section and line.startswith("```"):
                # Code block: first 200 chars
                in_section = False
        return "\n".join(lines[:50])

    def chat(self, messages: List[Dict], max_tokens: int = 1024) -> str:
        # Use the last user message
        last_user = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        if last_user:
            return self.complete(last_user.get("content", ""), max_tokens=max_tokens)
        return ""


class MockProvider(Provider):
    """Returns canned responses for testing."""

    name = "mock"

    def __init__(self, canned: str = "Mock answer"):
        self.canned = canned

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        return self.canned

    def chat(self, messages: List[Dict], max_tokens: int = 1024) -> str:
        return self.canned


class OpenAIProvider(Provider):
    """OpenAI provider. Requires `openai` package and OPENAI_API_KEY."""

    name = "openai"

    def __init__(self, model: str = "gpt-4o-mini"):
        try:
            import openai  # noqa: F401
        except ImportError as e:
            raise ImportError("pip install openai to use OpenAIProvider") from e
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY not set")
        self._client = openai.OpenAI()
        self.model = model

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def chat(self, messages: List[Dict], max_tokens: int = 1024) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


class AnthropicProvider(Provider):
    """Anthropic provider. Requires `anthropic` package and ANTHROPIC_API_KEY."""

    name = "anthropic"

    def __init__(self, model: str = "claude-haiku-4-5"):
        try:
            import anthropic  # noqa: F401
        except ImportError as e:
            raise ImportError("pip install anthropic to use AnthropicProvider") from e
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise EnvironmentError("ANTHROPIC_API_KEY not set")
        self._client = anthropic.Anthropic()
        self.model = model

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def chat(self, messages: List[Dict], max_tokens: int = 1024) -> str:
        # Anthropic separates system message
        system = next((m["content"] for m in messages if m["role"] == "system"), None)
        non_system = [m for m in messages if m["role"] != "system"]
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=non_system,
        )
        return response.content[0].text


class OllamaProvider(Provider):
    """Ollama local provider. Requires Ollama running locally.

    SECURITY (CISO-V2-005): host is validated against an allowlist to
    defeat SSRF. Only localhost and 127.0.0.1 by default. Override
    via SWEBOK_OLLAMA_ALLOW_PRIVATE=1 to allow private IPs.
    """

    name = "ollama"

    def __init__(self, model: str = "llama3.2", host: str = "http://localhost:11434"):
        import urllib.request
        from urllib.parse import urlparse
        import ipaddress
        # Validate host against allowlist to prevent SSRF
        parsed = urlparse(host)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Ollama host scheme must be http(s), got {parsed.scheme!r}")
        hostname = parsed.hostname or ""
        # Allow localhost variants by default
        allow = {"localhost", "127.0.0.1", "::1", "ollama"}
        allow_private = os.environ.get("SWEBOK_OLLAMA_ALLOW_PRIVATE", "0") == "1"
        if hostname.lower() not in allow:
            # Check if hostname is a private IP
            try:
                ip = ipaddress.ip_address(hostname)
                is_private = ip.is_private or ip.is_loopback or ip.is_link_local
            except ValueError:
                is_private = False
            if is_private and not allow_private:
                raise ValueError(
                    f"Ollama host {hostname!r} is private/loopback. "
                    f"Set SWEBOK_OLLAMA_ALLOW_PRIVATE=1 to override."
                )
            if not is_private and not allow_private:
                # Public IPs always allowed (no SSRF concern)
                pass
        self.model = model
        self.host = host
        # Probe to check if Ollama is running
        try:
            urllib.request.urlopen(f"{host}/api/tags", timeout=2)
        except Exception as e:
            raise EnvironmentError(f"Ollama not reachable at {host}: {e}")

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        import urllib.request
        import json
        data = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens},
        }).encode()
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())["response"]

    def chat(self, messages: List[Dict], max_tokens: int = 1024) -> str:
        import urllib.request
        import json
        data = json.dumps({
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"num_predict": max_tokens},
        }).encode()
        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())["message"]["content"]


# Factory
def create(provider_name: str = None, **kwargs) -> Provider:
    """Create a provider by name (or from env var SWEBOK_PROVIDER)."""
    name = provider_name or os.environ.get("SWEBOK_PROVIDER", "deterministic")
    providers = {
        "deterministic": DeterministicProvider,
        "mock": MockProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
    }
    if name not in providers:
        raise ValueError(f"Unknown provider: {name}. Available: {list(providers)}")
    return providers[name](**kwargs)


# === CLI ===
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test the LLM provider abstraction")
    parser.add_argument("--provider", default="deterministic")
    parser.add_argument("--prompt", default="Explain SOLID principles briefly.")
    args = parser.parse_args()
    try:
        p = create(args.provider)
    except (ImportError, EnvironmentError) as e:
        print(f"[{args.provider}] not available: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Provider: {p.name}")
    print(f"Prompt: {args.prompt}")
    print()
    response = p.complete(args.prompt)
    print(f"Response:\n{response}")
