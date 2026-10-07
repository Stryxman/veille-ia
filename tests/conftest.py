import pytest


@pytest.fixture(autouse=True)
def no_model_key(monkeypatch):
    # a key set on the development machine must never reach a test
    monkeypatch.delenv("LLM_API_KEY", raising=False)
